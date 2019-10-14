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
from store import RegularLine, ExpressLine, SelfServeLine, Customer, Item, \
    GroceryStore

GROCERY_STORE_2 = '{\n  "regular_count": 1,\n   "express_count": 1,\n   ' \
                  '"self_serve_count": 0,\n   "line_capacity": 1\n}'

# TODO: write your test functions for the checkout classes here


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
