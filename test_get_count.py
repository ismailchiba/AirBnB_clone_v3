#!/usr/bin/python3
"""Test .get() and .count() methods"""
from models import storage
from models.state import State

# Print the total count of all objects
print("All objects: {}".format(storage.count()))

# Print the count of all State objects
print("State objects: {}".format(storage.count(State)))

# Retrieve and print the first State object
all_states = storage.all(State)
if len(all_states) > 0:
    first_state_id = list(all_states.values())[0].id
    print("First state: {}".format(storage.get(State, first_state_id)))
else:
    print("No State objects found")