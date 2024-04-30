#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("id: {}".format(first_state_id))
print("First state: {}".format(storage.get(State, first_state_id)))
print("Second state: {}".format(storage.get(State, 28654652)))
print("third state: {}".format(storage.get(State)))
