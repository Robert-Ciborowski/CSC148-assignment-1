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

# Note: we need these imports to test the various functions of the lines
from store import Item, Customer, EXPRESS_LIMIT


def test_checkout_line_init() -> None:
    line = CheckoutLine(5)
    assert line.capacity == 5
    assert line.is_open
    assert line.queue == []


def test_checkout_line_len_empty() -> None:
    line = CheckoutLine(5)
    assert len(line) == 0


def test_checkout_line_len_non_empty() -> None:
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


def test_checkout_can_accept_has_room() -> None:
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert line.can_accept(jeff)


def test_checkout_can_accept_doesnt_have_room() -> None:
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('bananas', 1), Item('bananas', 1)]
    sofia = Customer('Sofia', item_list_2)
    line.accept(jeff)
    assert not line.can_accept(sofia)


def test_checkout_can_accept_closed() -> None:
    line = CheckoutLine(1)
    line.is_open = False
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert not line.can_accept(jeff)


def test_checkout_accept_has_room() -> None:
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert line.accept(jeff)


def test_checkout_accept_doesnt_have_room() -> None:
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('bananas', 1), Item('bananas', 1)]
    sofia = Customer('Sofia', item_list_2)
    line.accept(jeff)
    assert not line.accept(sofia)


def test_checkout_accept_closed() -> None:
    line = CheckoutLine(1)
    line.is_open = False
    item_list = [Item('bananas', 1), Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    assert not line.accept(jeff)


def test_checkout_start_checkout_empty() -> None:
    line = CheckoutLine(1)
    assert line.start_checkout() == 0


def test_checkout_start_checkout_non_empty() -> None:
    line = CheckoutLine(1)
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 6


def test_checkout_close_no_customers() -> None:
    line = CheckoutLine(3)
    assert line.close() == []


def test_checkout_close_one_customer() -> None:
    line = CheckoutLine(3)
    item_list = [Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.close() == []


def test_checkout_close_many_customers() -> None:
    line = CheckoutLine(3)
    item_list = [Item('bananas', 1)]
    jeff = Customer('Jeff', item_list)
    item_list_2 = [Item('apples', 1)]
    sofia = Customer('Sofia', item_list_2)
    item_list_3 = [Item('kiwis', 1)]
    aela = Customer('Aela', item_list_3)
    line.accept(jeff)
    line.accept(sofia)
    line.accept(aela)
    moved_customers = line.close()
    assert sofia in moved_customers and aela in moved_customers


def test_express_line_accept_enough_items() -> None:
    line = CheckoutLine(1)
    item_list = []

    for i in range(0, EXPRESS_LIMIT - 1):
        item_list.append(Item('bananas', 1))

    jeff = Customer('Jeff', item_list)
    assert line.accept(jeff)


def test_express_line_accept_too_many_items() -> None:
    line = ExpressLine(1)
    item_list = []

    for i in range(0, EXPRESS_LIMIT + 2):
        item_list.append(Item('bananas', 1))

    jeff = Customer('Jeff', item_list)
    assert not line.accept(jeff)


def test_self_serve_line_start_checkout_no_items() -> None:
    line = SelfServeLine(1)
    item_list = []
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 0


def test_self_serve_line_start_checkout_many_items() -> None:
    line = SelfServeLine(1)
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3)]
    jeff = Customer('Jeff', item_list)
    line.accept(jeff)
    assert line.start_checkout() == 12



def test_close_line() -> None:
    line = RegularLine(4)
    items = [Item('Bananas', 6)]
    c1 = Customer('Alice', items)
    c2 = Customer('Bob', items)
    c3 = Customer('Charlie', items)
    line.accept(c1)
    line.accept(c2)
    line.accept(c3)
    assert line.close() == [c2, c3]


def test_close_line_one_customer() -> None:
    line = RegularLine(4)
    items = [Item('Bananas', 6)]
    c1 = Customer('Alice', items)
    line.accept(c1)
    assert line.close() == []


def test_close_line_no_customers() -> None:
    line = RegularLine(4)
    assert line.close() == []


if __name__ == '__main__':
    import pytest
    pytest.main(['test_checkouts.py'])
