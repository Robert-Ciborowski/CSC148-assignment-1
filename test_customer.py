"""CSC148 Assignment 1: Tests for Customer

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for testing the Customer class.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from store import Customer, Item


def test_customer_init() -> None:
    """ Test customer initialization with correct name and items,
     and default arrival time.

    """
    item_list = [Item('bananas', 7)]
    belinda = Customer('Belinda', item_list)
    assert belinda.name == 'Belinda'
    assert belinda._items == item_list
    assert belinda.arrival_time == -1


def test_customer_num_items_empty() -> None:
    """ Test customer num_items when customer has no items.

    """
    item_list = []
    belinda = Customer('Belinda', item_list)
    assert belinda.num_items() == 0


def test_customer_num_items_many() -> None:
    """ Test customer num_items when customer has many items.

    """
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3),
                 Item('strawberries', 4), Item('guavas', 5), Item('oranges', 6)]
    belinda = Customer('Belinda', item_list)
    assert belinda.num_items() == 6
    assert len(belinda._items) == 6


def test_item_time_no_items() -> None:
    """ Test customer get_item_time when customer has no items.

    """
    item_list = []
    belinda = Customer('Belinda', item_list)
    assert belinda.get_item_time() == 0


def test_item_time_many_items() -> None:
    """ Test customer get_item_time when customer has many items.

    """
    item_list = [Item('bananas', 1), Item('apples', 2), Item('kiwis', 3),
                 Item('strawberries', 4), Item('guavas', 5), Item('oranges', 6)]
    belinda = Customer('Belinda', item_list)
    assert belinda.get_item_time() == 21
    assert len(belinda._items) == 6


if __name__ == '__main__':
    import pytest

    pytest.main(['test_customer.py'])

    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest', 'io',
                                   'store', 'pytest'],
        'disable': ['W0613', 'W0212']})
