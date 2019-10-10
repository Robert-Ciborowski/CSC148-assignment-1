"""CSC148 Assignment 1 - Modelling a Grocery Store (Task 1a)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the entities
in a grocery store.

This code is provided solely for the personal and private use of
students taking the CSC148 course at the University of Toronto.
Copying for purposes other than this use is expressly prohibited.
All forms of distribution of this code, whether as given or with
any changes, are expressly prohibited.

Author: Jacqueline Smith

All of the files in this directory and all subdirectories are:
Copyright (c) 2019 Jacqueline Smith
"""
from __future__ import annotations
from typing import List, Optional, TextIO
import json
from assignments.a1.container import PriorityQueue

# Use this constant in your code
EXPRESS_LIMIT = 7


# TODO: Complete the GroceryStore class and methods according to the docstrings
# You may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class GroceryStore:
    """A grocery store.
    === Attributes ===
    _regular_count: the number of regular checkout lines
    _express_count: the number of express checkout lines
    _self_serve_count: the number of self checkout lines
    _lines: the list of checkout lines
    """
    _regular_count: int
    _express_count: int
    _self_serve_count: int
    _lines: [CheckoutLine]

    def __init__(self, config_file: TextIO) -> None:
        """Initialize a GroceryStore from a configuration file <config_file>.
        """
        text = ""
        self._lines = []
        for str in config_file:
            text += str
        j = json.loads(text)
        self._regular_count = j['regular_count']
        self._express_count = j['express_count']
        self._self_serve_count = j['self_serve_count']
        line_capacity = j['line_capacity']
        # review this to avoid off by one errors
        i = 0
        while i < self._regular_count:
            self._lines.append(RegularLine(line_capacity))
            i += 1
        i = 0
        while i < self._express_count:
            self._lines.append(ExpressLine(EXPRESS_LIMIT))
            i += 1
        i = 0
        while i < self._self_serve_count:
            self._lines.append(SelfServeLine(line_capacity))
            i += 1

    def enter_line(self, customer: Customer) -> int:
        """Pick a new line for <customer> to join.

        Return the index of the line that the customer joined.
        Must use the algorithm from the handout.

        Return -1 if there is no line available for the customer to join.
        """
        # I introduced _lines, is the index of the line there the same index
        # that's referred to in the docstring?

        # arbitrary BIG length
        smallest_length = 8000000000
        index = -1
        for i in range(len(self._lines)):
            curr_length = len(self._lines[i])
            if curr_length == self._lines[i].capacity:
                continue
            if curr_length < smallest_length:
                smallest_length = curr_length
                index = i
        return index

    def line_is_ready(self, line_number: int) -> bool:
        """Return True iff checkout line <line_number> is ready to start a
        checkout.
        """
        # does this mean when the checkout line can accept a new customer or
        # when it is ready to process the first customer in the queue?

        # maybe along the latter lines it refers to enough time having passed
        # since the previously processed customer

        # even though the latter feels like a better description of the
        # header, I'm gonna implement the former as it seems to match the
        # other methods in this class
        return self._lines[line_number].can_accept()

    def start_checkout(self, line_number: int) -> int:
        """Return the time it will take to check out the next customer in
        line <line_number>
        """
        return self._lines[line_number].start_checkout()

    def complete_checkout(self, line_number: int) -> int:
        """Return the number of customers remaining to be checked out in line
        <line_number>
        """
        # I don't see yet how the function described in the docstring relates
        # to completing the checkout

        return len(self._lines[line_number])

    def close_line(self, line_number: int) -> List[Customer]:
        """Close checkout line <line_number> and return the customers from
        that line who are still waiting to be checked out.
        """

        return self._lines[line_number].close()

    def get_first_in_line(self, line_number: int) -> Optional[Customer]:
        """Return the first customer in line <line_number>, or None if there
        are no customers in line.
        """
        if not len(self._lines[line_number].queue) == 0:
            return self._lines[line_number].queue[0]
        return None


# TODO: Complete the methods in Customer according to their docstrings
# You should use the existing attributes in your solution. However, if you need
# to, you may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class Customer:
    """A grocery store customer.

    === Attributes ===
    name: A unique identifier for this customer.
    arrival_time: The time this customer joined a line.
    _items: The items this customer has.

    === Representation Invariant ===
    arrival_time >= 0 if this customer has joined a line, and -1 otherwise
    """
    name: str
    arrival_time: int
    _items: List[Item]

    def __init__(self, name: str, items: List[Item]) -> None:
        """Initialize a customer with the given <name>, an initial arrival time
         of -1, and a copy of the list <items>.

        >>> item_list = [Item('bananas', 7)]
        >>> belinda = Customer('Belinda', item_list)
        >>> belinda.name
        'Belinda'
        >>> belinda._items == item_list
        True
        >>> belinda.arrival_time
        -1
        """
        self.name = name
        self._items = items
        self.arrival_time = -1

    def num_items(self) -> int:
        """Return the number of items this customer has.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.num_items()
        2
        """
        return len(self._items)

    def get_item_time(self) -> int:
        """Return the number of seconds it takes to check out this customer.

        >>> c = Customer('Bo', [Item('bananas', 7), Item('cheese', 3)])
        >>> c.get_item_time()
        10
        """
        time = 0
        for item in self._items:
            time += item.get_time()
        return time


class Item:
    """A class to represent an item to be checked out.

    Do not change this class.

    === Attributes ===
    name: the name of this item
    _time: the amount of time it takes to checkout this item
    """
    name: str
    _time: int

    def __init__(self, name: str, time: int) -> None:
        """Initialize a new time with <name> and <time>.

        >>> item = Item('bananas', 7)
        >>> item.name
        'bananas'
        >>> item._time
        7
        """
        self.name = name
        self._time = time

    def get_time(self) -> int:
        """Return how many seconds it takes to checkout this item.

        >>> item = Item('bananas', 7)
        >>> item.get_time()
        7
        """
        return self._time


# TODO: Complete the CheckoutLine class and methods according to the docstrings
# Do not add any new attributes or methods (public or private) to this class.
class CheckoutLine:
    """A checkout line in a grocery store.

    This is an abstract class; subclasses are responsible for implementing
    start_checkout().

    === Attributes ===
    capacity: The number of customers allowed in this CheckoutLine.
    is_open: True iff the line is open.
    queue: Customers in this line in FIFO order. Front of queue is at index 0

    === Representation Invariants ===
    - Each customer in this line has not been checked out yet.
    - The number of customers is less than or equal to capacity.
    """
    capacity: int
    is_open: bool
    queue: List[Customer]

    def __init__(self, capacity: int) -> None:
        """Initialize an open and empty CheckoutLine.

        >>> line = CheckoutLine(1)
        >>> line.capacity
        1
        >>> line.is_open
        True
        >>> line.queue
        []
        """
        self.is_open = True
        self.queue = []
        self.capacity = capacity

    def __len__(self) -> int:
        """Return the size of this CheckoutLine.
        """
        return len(self.queue)

    def can_accept(self, customer: Customer) -> bool:
        """Return True iff this CheckoutLine can accept <customer>.
        """
        if not self.is_open:
            return False
        if len(self) < self.capacity:
            return True
        return False

    def accept(self, customer: Customer) -> bool:
        """Accept <customer> at the end of this CheckoutLine.
        Return True iff the customer is accepted.

        >>> line = CheckoutLine(1)
        >>> c1 = Customer('Belinda', [Item('cheese', 3)])
        >>> c2 = Customer('Hamman', [Item('chips', 4), Item('gum', 1)])
        >>> line.accept(c1)
        True
        >>> line.accept(c2)
        False
        >>> line.queue == [c1]
        True
        """
        if not self.can_accept():
            return False
        self.queue.append(customer)
        return True

    def start_checkout(self) -> int:
        """Checkout the next customer in this CheckoutLine.

        Return the time it will take to checkout the next customer.
        """
        # does not mutate queue
        # this assumes self.queue is non empty
        # TODO: Add a precondition saying it should not be empty??????
        # Or are we not allowed to modify headers.
        if len(self.queue) == 0:
            return 0
        return self.queue[0].get_item_time()

    def complete_checkout(self) -> bool:
        """Finish the checkout for this CheckoutLine.

        Return whether there are any remaining customers in the line.
        """
        return self.queue != []

    def close(self) -> List[Customer]:
        """Close this line.

        Return a list of all customers that need to be moved to another line.
        """
        # Also mutates queue
        moved_customers = []
        self.is_open = False
        # if we don't want to mutate queue, just traverse self.queue and
        # append each to moved_customers
        for i in range(len(self) - 1):
            moved_customers.append(self.queue.pop())
        return moved_customers


# TODO: implement the following subclasses of CheckoutLine
# Only implement those methods that cannot be used exactly as inherited
# from the superclass.
# You may add private attributes and helper methods, but do not change the
# public interface of the subclasses.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.

class RegularLine(CheckoutLine):
    """A regular CheckoutLine."""


class ExpressLine(CheckoutLine):
    """An express CheckoutLine.

    Has a limit of EXPRESS_LIMIT customers in line.
    """

    def can_accept(self, customer: Customer) -> bool:
        if len(self) < EXPRESS_LIMIT:
            return CheckoutLine.can_accept(self, customer)
        return False


class SelfServeLine(CheckoutLine):
    """A self-serve CheckoutLine.

    Takes twice as long to check out.
    """

    def start_checkout(self) -> int:
        return 2 * CheckoutLine.start_checkout(self)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
    import python_ta

    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'json',
                                   'python_ta', 'doctest'],
        'disable': ['W0613']})
