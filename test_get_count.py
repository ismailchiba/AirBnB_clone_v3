#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

# Create some new state objects for testing
state1 = State(name="California")
state1.save()
state2 = State(name="Texas")
state2.save()

# Test count method
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

# Test get method
first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))
