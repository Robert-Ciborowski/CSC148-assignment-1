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
    store = GroceryStore(GROCERY_STORE_2)
    assert store.line_is_ready(0)
    assert store.line_is_ready(1)
    pass

if __name__ == '__main__':
    import pytest

    pytest.main(['test_grocerystore.py'])
