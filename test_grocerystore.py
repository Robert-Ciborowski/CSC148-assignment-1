"""CSC148 Assignment 1: Tests for GroceryStore

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the GroceryStore class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from io import StringIO
from store import GroceryStore, Customer, Item, EXPRESS_LIMIT

GROCERY_STORE = '{\n  "regular_count": 3,\n   "express_count": 2,\n   ' \
                '"self_serve_count": 4,\n   "line_capacity": 10\n}'

GROCERY_STORE_1_LINE_1_CAP = '{\n  "regular_count": 1,\n   "express_count": ' \
                             '0,\n   "self_serve_count": 0,\n   ' \
                             '"line_capacity": 1\n} '

GROCERY_STORE_2_LINES_2_CAP = '{\n  "regular_count": 1,\n   "express_count": ' \
                              '0,\n   "self_serve_count": 1,\n   ' \
                              '"line_capacity": 2\n} '

GROCERY_STORE_1_LINE_2_CAP = '{\n  "regular_count": 1,\n   "express_count": ' \
                             '0,\n   "self_serve_count": 0,\n   ' \
                             '"line_capacity": 2\n} '

GROCERY_STORE_EXPRESS = '{\n  "regular_count": 0,\n   "express_count": 1,' + \
                        '\n   "self_serve_count": 0,\n   "line_capacity": 2\n}'


# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.

def test_grocery_store_init() -> None:
    """ Test store initialization with correct lines."""
    store = GroceryStore(StringIO(GROCERY_STORE))
    assert store._regular_count == 3
    assert store._express_count == 2
    assert store._self_serve_count == 4
    assert len(store._lines) == 9
    for line in store._lines:
        assert line.capacity == 10


def test_enter_line() -> None:
    """ Test whether customer enters correct line with empty lines."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    assert len(store._lines[0]) == 0
    assert store.enter_line(belinda) == 0
    assert len(store._lines[0]) == 1


def test_enter_line_lines_full() -> None:
    """ Test whether customer enters line with full line(s)."""
    store = GroceryStore(GROCERY_STORE_1_LINE_1_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 5)]
    arnold = Customer('Arnold', item_list_2)
    store.enter_line(arnold)
    assert store.enter_line(belinda) == -1


def test_enter_first_occupied() -> None:
    """ Test whether customer enters correct line when first is occupied."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 5)]
    arnold = Customer('Arnold', item_list_2)
    store.enter_line(arnold)
    assert store.enter_line(belinda) == 1


def test_enter_over_express_limit() -> None:
    """ Test whether customer enters express line when they have too
    many items."""
    store = GroceryStore(GROCERY_STORE_EXPRESS)
    item_list = [Item('apples', 5)]
    for i in range(EXPRESS_LIMIT):
        item_list.append(Item('apples', i))
    arnold = Customer('Arnold', item_list)
    store.enter_line(arnold)
    assert store.enter_line(arnold) == -1
    # poor guy


def test_enter_line_lines_occupied() -> None:
    """ Test whether customer enters a line with another customer in it."""
    store = GroceryStore(GROCERY_STORE_2_LINES_2_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 5)]
    arnold = Customer('Arnold', item_list_2)
    item_list_3 = [Item('carrots', 3)]
    charlie = Customer('Charlie', item_list_3)
    store.enter_line(arnold)
    store.enter_line(belinda)
    assert store.enter_line(charlie) == 0
    assert len(store._lines[0]) == 2


def test_line_is_ready_one_occupant() -> None:
    """ Test line is ready with exactly one customer."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert store.line_is_ready(0)


def test_is_ready_more_occupants() -> None:
    """ Test line is ready with more than one customer."""
    store = GroceryStore(GROCERY_STORE_1_LINE_2_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 5)]
    arnold = Customer('Arnold', item_list_2)
    store.enter_line(belinda)
    store.enter_line(arnold)
    assert not store.line_is_ready(0)


def test_line_is_ready_empty_line() -> None:
    """ Test line is ready with no customers."""
    store = GroceryStore(GROCERY_STORE)
    assert not store.line_is_ready(0)


def test_start_checkout_empty() -> None:
    """ Test whether empty line starts checkout."""
    store = GroceryStore(GROCERY_STORE)
    assert store.start_checkout(0) == 0


def test_start_checkout_non_empty() -> None:
    """ Test whether non empty line starts checkout."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6), Item('apples', 5), Item('carrots', 3)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert store.start_checkout(0) == 14


def test_complete_checkout_empty() -> None:
    """ Test whether customers left to checkout after checkout when
    line is empty."""
    store = GroceryStore(GROCERY_STORE)
    assert not store.complete_checkout(0)


def test_complete_checkout_one() -> None:
    """ Test whether customers left to checkout after checkout when
    line has one customer."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert not store.complete_checkout(0)


def test_complete_checkout_more() -> None:
    """ Test whether customers left to checkout after checkout when
    line is empty."""
    store = GroceryStore(GROCERY_STORE_1_LINE_2_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    charlie = Customer('Charlie', item_list)
    store.enter_line(belinda)
    store.enter_line(charlie)
    assert store.complete_checkout(0)


def test_close_line_empty() -> None:
    """ Test whether empty line returns customers on close."""
    store = GroceryStore(GROCERY_STORE)
    assert store.close_line(0) == []


def test_close_line_one_customer() -> None:
    """ Test whether line with one customer returns customers on close."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert store.close_line(0) == []


def test_close_line_more_occupants() -> None:
    """ Test whether line with more than one customer returns correct
    customers on close."""
    store = GroceryStore(GROCERY_STORE_1_LINE_2_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    item_list_2 = [Item('cherries', 5)]
    charlie = Customer('Charlie', item_list_2)
    store.enter_line(charlie)
    assert store.close_line(0) == [charlie]


def test_get_first_in_line_many() -> None:
    """ Test whether get first in line returns correct customer with
    one customer in line."""
    store = GroceryStore(GROCERY_STORE)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert store.get_first_in_line(0) == belinda


def test_get_first_in_line_one() -> None:
    """ Test whether get first in line returns correct customer with
    more than one customer in line."""
    store = GroceryStore(GROCERY_STORE_1_LINE_2_CAP)
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    item_list_2 = [Item('cherries', 5)]
    charlie = Customer('Charlie', item_list_2)
    store.enter_line(charlie)
    assert store.get_first_in_line(0) == belinda


def test_get_first_in_line_empty() -> None:
    """ Test whether get first in line returns correct customer with
    empty line."""
    store = GroceryStore(GROCERY_STORE)
    assert store.get_first_in_line(0) is None


if __name__ == '__main__':
    import pytest

    pytest.main(['test_grocerystore.py'])

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest', 'io',
                                   'store', 'pytest'],
        'disable': ['W0613', 'W0212']})
