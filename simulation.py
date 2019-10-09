"""Assignment 1 - Grocery Store Simulation (Task 3)

=== CSC148 Fall 2019 ===
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains a class to simulate a grocery store, as well as some
example testing code.

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
from typing import Dict, Any, TextIO
from event import create_event_list, CustomerArrival, CheckoutCompleted
from store import GroceryStore
from container import PriorityQueue


class GroceryStoreSimulation:
    """A Grocery Store simulation.

    This is the class which is responsible for setting up and running a
    simulation. The interface is given to you: your main task is to implement
    the two methods according to their docstrings.

    Of course, you may add whatever private attributes you want to this class.
    Because you should not change the interface in any way, you may not add
    any public attributes.

    === Private Attributes ===
    _events: A sequence of events arranged in priority determined by the event
             sorting order.
    _store: The store being simulated.
    """
    _events: PriorityQueue
    _store: GroceryStore

    def __init__(self, store_file: TextIO) -> None:
        """Initialize a GroceryStoreSimulation using configuration <store_file>.
        """
        self._events = PriorityQueue()
        self._store = GroceryStore(store_file)

    def run(self, file: TextIO) -> Dict[str, Any]:
        """Run the simulation on the events stored in <initial_events>.

        Return a dictionary containing statistics of the simulation,
        according to the specifications in the assignment handout.
        """
        # I think they mean <self._events> instead of <initial_events>
        # I don't know what <initial_events> is

        # Initialize statistics
        stats = {
            'num_customers': 0,
            'total_time': 0,
            'max_wait': -1
        }
        # outlining steps

        # fill self._events from file
        self._events = create_event_list(file)

        # we will track each customer's arrival and departure times
        # I am assuming each customer has a unique id in memory,
        # ie no one customer has two customer objects
        # (also assuming that no two customers have same id,
        # but this seems reasonable)
        customers = {}
        # do all events
        while not self._events.is_empty():
            # calculate statistics

            # get next event
            current_event = self._events.remove()

            # I think the event timestamp is the current time
            stats['total_time'] = self._events.remove().timestamp

            if isinstance(current_event, CustomerArrival):
                stats['num_customers'] += 1
                customers[current_event.customer] = \
                    [current_event.timestamp, -1]
            elif isinstance(current_event, CheckoutCompleted):
                customers[current_event.customer][1] = current_event.timestamp

            #  calculate max wait time
            for customer in customers:
                wait_time = customer[1] - customer[0]
                if wait_time > stats['max_wait']:
                    stats['max_wait'] = wait_time

            # I think we need to track each customer,
            # to monitor their wait times

            # do we track from arrival or from joining line?
            # assuming arrival

        # TODO: test these stats

        return stats


# We have provided a bit of code to help test your work.
if __name__ == '__main__':
    config_file = open('input_files/config_111_01.json')
    sim = GroceryStoreSimulation(config_file)
    config_file.close()
    event_file = open('input_files/events_one.txt')
    sim_stats = sim.run(event_file)
    event_file.close()
    print(sim_stats)
    import doctest
    doctest.testmod()
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['__future__', 'typing', 'event', 'store',
                                   'container', 'python_ta', 'doctest']})
