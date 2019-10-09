"""Assignment 1 - Events (Task 2)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains all of the classes necessary to model the different
kinds of events in the simulation.

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
from typing import List, TextIO
from store import GroceryStore, Customer, Item


class Event:
    """An event.

    Events have an ordering based on the event timestamp in non-ascending
    order. Events with older timestamps are greater than those with newer
    timestamps.

    This class is abstract; subclasses must implement do().

    YOU SHOULD NOT CHANGE THIS CLASS!

    === Attributes ===
    timestamp: A timestamp for this event.
    """
    timestamp: int

    def __init__(self, timestamp: int) -> None:
        """Initialize an Event with a given timestamp.

        Precondition: timestamp must be a non-negative integer.

        >>> Event(7).timestamp
        7
        """
        self.timestamp = timestamp

    # The following six 'magic methods' are overridden to allow for easy
    # comparison of Event instances. All comparisons simply perform the
    # same comparison on the 'timestamp' attribute of the two events.
    def __eq__(self, other: Event) -> bool:
        """Return whether this Event is equal to <other>.

        Two events are equal if they have the same timestamp.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first == second
        False
        >>> second.timestamp = first.timestamp
        >>> first == second
        True
        """
        return self.timestamp == other.timestamp

    def __ne__(self, other: Event) -> bool:
        """Return True iff this Event is not equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first != second
        True
        >>> second.timestamp = first.timestamp
        >>> first != second
        False
        """
        return not self.__eq__(other)

    def __lt__(self, other: Event) -> bool:
        """Return True iff this Event is less than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first < second
        True
        >>> second < first
        False
        """
        return self.timestamp < other.timestamp

    def __le__(self, other: Event) -> bool:
        """Return True iff this Event is less than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first <= first
        True
        >>> first <= second
        True
        >>> second <= first
        False
        """
        return self.timestamp <= other.timestamp

    def __gt__(self, other: Event) -> bool:
        """Return True iff this Event is greater than <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first > second
        False
        >>> second > first
        True
        """
        return not self.__le__(other)

    def __ge__(self, other: Event) -> bool:
        """Return True iff this Event is greater than or equal to <other>.

        >>> first = Event(1)
        >>> second = Event(2)
        >>> first >= first
        True
        >>> first >= second
        False
        >>> second >= first
        True
        """
        return not self.__lt__(other)

    def do(self, store: GroceryStore) -> List[Event]:
        """Return a list of events generated by performing this event.

        Call methods on <store> to update its state according to the
        meaning of the event. Note: the "business logic" of what actually
        happens inside a grocery store should be handled in the GroceryStore
        class, not in any Event classes.

        Return a list of new events spawned by this event (making sure the
        timestamps are correct).
        """
        raise NotImplementedError('Implemented in a subclass')


# TODO: Complete the subclasses for the different types of events below.
# You should use the provided attributes in your solution. However, if you need
# to, you may add private attributes and helper methods, but do not change the
# public interface.
# Write docstrings for all methods you write, and document your attributes
# in the class docstring.
class CustomerArrival(Event):
    """A customer arrives at the checkout area ready to check out.

    === Attributes ===
    customer: The arriving customer
    """
    customer: Customer

    def __init__(self, timestamp: int, c: Customer) -> None:
        """Initialize a CustomerArrival event with <timestamp> and customer <c>.
        """
        Event.__init__(self, timestamp)
        self.customer = c

    def do(self, store: GroceryStore) -> List[Event]:
        line = store.enter_line(self.customer)

        if line == -1:
            # This event needs to be reprocessed at a later time.
            self.timestamp += 1
            return [self]
        else:
            timestamp = 0

            if store.get_first_in_line(line) is None:
                return [CheckoutStarted(timestamp, line)]

            return []


class CheckoutStarted(Event):
    """A customer starts the checkout process.

    Once the checkout process starts, the only way for the customer to leave
    the line is for a CheckoutCompleted event to occur.

    === Attributes ===
    line_number: The number of the checkout line.
    """
    # this docstring gives a clue to start_checkout in store.py
    line_number: int

    def __init__(self, timestamp: int, line_number: int) -> None:
        """Initialize a CheckoutStarted event with <timestamp> and
        <line_number>.
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number

        assert 1 == 0

    def do(self, store: GroceryStore) -> List[Event]:
        customer = store.get_first_in_line(self._line_number)
        duration = store.start_checkout(self.line_number)
        return [CheckoutCompleted(self.timestamp + duration, self.line_number,
                                  customer)]

class CheckoutCompleted(Event):
    """A customer finishes the checkout process.

    A CheckoutCompleted event might occur after a line closes.

    === Attributes ===
    line_number: The number of the checkout line.
    customer: The finishing customer.
    """
    line_number: int
    customer: Customer

    def __init__(self, timestamp: int, line_number: int, c: Customer) -> None:
        """Initialize a CheckoutCompleted event with <timestamp>, <line_number>,
        and customer <c>.
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number
        self.customer = c

    def do(self, store: GroceryStore) -> List[Event]:
        # If a customer finishes checking out, the next customer in the line (if
        # there is one) gets a “begin checking out” event with the same
        # timestamp as the “finish” event.
        remaining = store.complete_checkout(self.line_number)

        if remaining == 0:
            return []

        return [CheckoutStarted(self.timestamp, self.line_number)]


class CloseLine(Event):
    """A CheckoutLine gets closed.

    === Attributes ===
    line_number: The number of the checkout line.
    """
    line_number: int

    def __init__(self, timestamp: int, line_number: int) -> None:
        """Initialize a CloseLine event with <timestamp> and <line_number>.
        """
        Event.__init__(self, timestamp)
        self.line_number = line_number

    def do(self, store: GroceryStore) -> List[Event]:
        assert 1 == 0
        # A line closes. All customers who were in the line must join a new
        # line, except the first customer in the line. No new customers may join
        # the line after it has closed.
        # If a line closes, there is one “new customer” event per customer in
        # the checkout line after the first one. The new events should be spaced
        # 1 second apart, with the last customer in the line having the earliest
        # “new customer” event, which is the same as the “line close” event.
        customers = store.close_line(self.line_number)
        events = []
        count = 0

        for i in range(len(customers), 1, -1):
            customer = customers[i]
            events.append(CustomerArrival(self.timestamp + count, customer))
            count += 1
        return events


def create_event_list(event_file: TextIO) -> List[Event]:
    """Return a list of Events based on raw list of events in <event_file>.

    Precondition: <event_file> is in the format specified by the assignment
    handout.
    """
    events = []

    for line in event_file.readlines():
        data = line.split(" ")
        event_type = data[1]

        if event_type == "Close":
            events.append(CloseLine(int(data[0])))
        elif event_type == "Arrive":
            items = []

            for i in range(3, len(data), 2):
                item = Item(data[i], int(data[i + 1]))
                items.append(item)

            customer = Customer(data[2], items)
            events.append(CustomerArrival(customer, int(data[0])))

if __name__ == '__main__':
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'store',
                                   'python_ta', 'doctest']})
