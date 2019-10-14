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
from store import GroceryStore, Customer, Item

GROCERY_STORE = '{\n  "regular_count": 3,\n   "express_count": 2,\n   ' \
                '"self_serve_count": 4,\n   "line_capacity": 10\n}'

GROCERY_STORE_2 = '{\n  "regular_count": 1,\n   "express_count": 1,\n   ' \
                  '"self_serve_count": 0,\n   "line_capacity": 1\n}'

GROCERY_STORE_3 = '{\n  "regular_count": 1,\n   "express_count": 1,\n   ' \
                  '"self_serve_count": 1,\n   "line_capacity": 2\n}'

GROCERY_STORE_4 = '{\n  "regular_count": 1,\n   "express_count": 0,\n   ' \
                  '"self_serve_count": 0,\n   "line_capacity": 2\n}'

EXPRESS_LIMIT = 7


# TODO: write your test functions for GroceryStore here
# Note - your tests should use StringIO to simulate opening a configuration file
# rather than requiring separate files.
# See the Assignment 0 sample test for an example of using StringIO in testing.

def test_grocery_store_init() -> None:
    store = GroceryStore(StringIO(GROCERY_STORE))
    assert store._regular_count == 3
    assert store._express_count == 2
    assert store._self_serve_count == 4
    assert len(store._lines) == 9
    for line in store._lines:
        assert line._capacity == 10


def test_enter_line() -> None:
    # Todo: this tests many properties of enter_line, split up test cases
    store = GroceryStore(StringIO(GROCERY_STORE_2))
    item_list = [Item('bananas', 7), Item('bananas', 7), Item('bananas', 7),
                 Item('bananas', 7), Item('bananas', 7), Item('bananas', 7),
                 Item('bananas', 7), Item('bananas', 7)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 6)]
    arnold = Customer('Arnold', item_list_2)
    item_list_3 = [Item('carrots', 5), Item('carrots', 5), Item('carrots', 5),
                   Item('carrots', 5), Item('carrots', 5), Item('carrots', 5),
                   Item('carrots', 5), Item('carrots', 5)]
    charlie = Customer('Charlie', item_list_3)
    item_list_4 = [Item('dandelions', 2)]
    david = Customer('David', item_list_4)
    elijah = Customer('Elijah', item_list)
    assert store.enter_line(belinda) == 0
    assert store.enter_line(charlie) == -1
    assert store.enter_line(arnold) == 1
    assert store.enter_line(david) == -1
    assert store.enter_line(elijah) == -1
    # taking for granted that lines work properly


def test_line_is_ready() -> None:
    store = GroceryStore(GROCERY_STORE)
    assert len(store._lines) == 9
    assert not store.line_is_ready(0)
    assert not store.line_is_ready(1)
    assert not store.line_is_ready(2)
    assert len(store._lines) == 9
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    arnold = Customer('Arnold', item_list)
    charlie = Customer('Charlie', item_list)
    store._lines[1].accept(belinda)
    store._lines[2].accept(charlie)
    store._lines[2].accept(arnold)
    assert not store.line_is_ready(0)
    assert store.line_is_ready(1)
    assert not store.line_is_ready(2)
    assert len(store._lines) == 9


def test_start_checkout() -> None:
    store = GroceryStore(GROCERY_STORE_3)
    assert store.start_checkout(0) == 0
    assert len(store._lines[0]) == 0
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    item_list_2 = [Item('apples', 6), Item('bananas', 5), Item('oranges', 4)]
    charlie = Customer('Charlie', item_list_2)
    store.enter_line(belinda)
    store.enter_line(charlie)
    daniel = Customer('Daniel', item_list)
    store._lines[0].accept(daniel)
    assert store.start_checkout(0) == 6
    assert store.start_checkout(1) == 15
    assert len(store._lines[0]) == 2
    assert len(store._lines[1]) == 1
    assert len(store._lines[2]) == 0


def test_complete_checkout() -> None:
    store = GroceryStore(GROCERY_STORE_4)
    assert store.complete_checkout(0) is False
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    charlie = Customer('Charlie', item_list)
    store.enter_line(charlie)
    assert store.complete_checkout(0) is True
    assert store.complete_checkout(0) is False


def test_close_line() -> None:
    store = GroceryStore(GROCERY_STORE_3)
    item_list = [Item('bananas', 6)]
    item_list_2 = [Item('cherries', 5)]
    item_list_3 = [Item('apples', 4)]
    belinda = Customer('Belinda', item_list)
    assert len(store.close_line(0)) == 0
    store.enter_line(belinda)
    assert len(store.close_line(1)) == 0
    charlie = Customer('Charlie', item_list_2)
    avery = Customer('Avery', item_list_3)
    store.enter_line(charlie)
    store.enter_line(avery)
    assert len(store.close_line(2)) == 1


def test_get_first_in_line() -> None:
    store = GroceryStore(GROCERY_STORE_2)
    assert store.get_first_in_line(0) is None
    item_list = [Item('bananas', 6)]
    belinda = Customer('Belinda', item_list)
    store.enter_line(belinda)
    assert store.get_first_in_line(0) == belinda


if __name__ == '__main__':
    import pytest

    pytest.main(['test_grocerystore.py'])
