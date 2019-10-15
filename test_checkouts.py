"""CSC148 Assignment 1: Tests for checkout classes

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the checkout classes.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import CheckoutLine, RegularLine, ExpressLine, SelfServeLine

# TODO: review Piazza to see how to fix this.
# Note: we need these imports to test the various functions of the lines
from store import Item, Customer, EXPRESS_LIMIT

# Also note: ExpressLine overrides can_accept, and SelfServeLine overrides
# start_checkout.
# Everything else is tested as an abstract CheckoutLine.


def test_checkout_line_init() -> None:
    """ Test abstract line initialization for correct capacity,
    openness and queue.

    """
    line = CheckoutLine(5)
    assert line.capacity == 5
    assert line.is_open
    assert line.queue == []


def test_children_init() -> None:
    """ Test all three line types for correct initialization.
    """
    line1 = RegularLine(5)
    assert line1.capacity == 5
    assert line1.is_open
    assert line1.queue == []
    line2 = ExpressLine(5)
    assert line2.capacity == 5
    assert line2.is_open
    assert line2.queue == []
    line3 = SelfServeLine(5)
    assert line3.capacity == 5
    assert line3.is_open
    assert line3.queue == []


def test_len_empty() -> None:
    """ Test length of line when it is empty."""
    line = CheckoutLine(5)
    assert len(line) == 0


def test_len_non_empty() -> None:
    """ Test length of line when it has customers."""
    line = CheckoutLine(5)
    item_list = [Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('apples', 1)]
    sofia = Customer('Sofia', item_list_2)
    item_list_3 = [Item('kiwis', 1)]
    aela = Customer('Aela', item_list_3)
    line.accept(jeff)
    line.accept(sofia)
    line.accept(aela)
    assert len(line) == 3


def test_can_accept_has_room() -> None:
    """ Test whether line can accept when it has room."""
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert line.can_accept(jeff)


def test_can_accept_no_room() -> None:
    """ Test whether line can accept when it doesn't have room."""
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('bananas', 1), Item('bananas', 1)]
    sofia = Customer('Sofia', item_list_2)
    line.accept(jeff)
    assert not line.can_accept(sofia)


def test_can_accept_closed() -> None:
    """ Test whether line can accept when it is closed."""
    line = CheckoutLine(1)
    line.is_open = False
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert not line.can_accept(jeff)


def test_accept_has_room() -> None:
    """ Test whether line accepts when it has room."""
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert line.accept(jeff)
    assert len(line) == 1


def test_accept_no_room() -> None:
    """ Test whether line accepts when it doesn't have room."""
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('bananas', 1), Item('bananas', 1)]
    sofia = Customer('Sofia', item_list_2)
    line.accept(jeff)
    assert not line.accept(sofia)
    assert len(line) == 1


def test_accept_closed() -> None:
    """ Test whether line accepts when it is closed."""
    line = CheckoutLine(1)
    line.is_open = False
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert not line.accept(jeff)


def test_start_checkout_empty() -> None:
    """ Test how many customers are left when an empty line starts checkout."""
    line = CheckoutLine(1)
    assert line.start_checkout() == 0


def test_start_checkout_non_empty() -> None:
    """ Test how many customers are left when a line with a customer
    starts checkout."""
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 6


def test_start_checkout_two_in_line() -> None:
    """ Test how many customers are left when a line with more than one customer
    starts checkout."""
    line = CheckoutLine(2)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('bananas', 1), Item('bananas', 1)]
    sofia = Customer('Sofia', item_list_2)
    line.accept(jeff)
    line.accept(sofia)
    assert line.start_checkout() == 2


def test_close_no_customers() -> None:
    """ Test whether customers are returned when empty line closes."""
    line = CheckoutLine(3)
    assert line.close() == []


def test_close_one_customer() -> None:
    """ Test whether customers are returned when a line with one customer
    closes."""
    line = CheckoutLine(3)
    item_list = [Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.close() == []


def test_close_many_customers() -> None:
    """ Test whether correct customers are returned when line with more than
    one customer closes."""
    line = CheckoutLine(3)
    item_list = [Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('apples', 2)]
    sofia = Customer('Sofia', item_list_2)
    item_list_3 = [Item('kiwis', 1)]
    aela = Customer('Aela', item_list_3)
    line.accept(jeff)
    line.accept(sofia)
    line.accept(aela)
    moved_customers = line.close()
    assert moved_customers == [sofia, aela]


def test_express_accept() -> None:
    """ Test whether an express line accepts a customer with less than the limit
     of items."""
    line = CheckoutLine(1)
    item_list = []

    for i in range(0, EXPRESS_LIMIT - 1):
        item_list.append(Item('bananas', i))

    jeff = Customer('Jeff', item_list)
    assert line.accept(jeff)


def test_express_too_many_items() -> None:
    """ Test whether an express line accepts a customer with more than the limit
     of items."""
    line = ExpressLine(1)
    item_list = []

    for i in range(0, EXPRESS_LIMIT + 2):
        item_list.append(Item('bananas', i))

    jeff = Customer('Jeff', item_list)
    assert not line.accept(jeff)


def test_self_checkout_no_items() -> None:
    """ Test self serve line checkout time for customer with no items."""
    line = SelfServeLine(1)
    item_list = []
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 0


def test_self_checkout_many_items() -> None:
    """ Test self serve line checkout time for customer with many items."""
    line = SelfServeLine(1)
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 12


def test_close_line_one_customer() -> None:
    """ Test whether close line returns customers when only one customer
    is in the line."""
    line = CheckoutLine(4)
    items = [Item('Bananas', 6)]
    c1 = Customer('Alice', items)
    line.accept(c1)
    assert line.close() == []


def test_close_line_no_customers() -> None:
    """ Test whether close line returns customers when no customers
    are in the line."""
    line = CheckoutLine(4)
    assert line.close() == []


if __name__ == '__main__':
    import pytest
    pytest.main(['test_checkouts.py'])

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest', 'io',
                                   'store', 'pytest'],
        'disable': ['W0613', 'W0212']})
