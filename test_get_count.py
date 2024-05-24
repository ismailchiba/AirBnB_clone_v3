#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State

all_objects = storage.all()
state_objects = storage.all(State)

print(f"All objects: {len(all_objects)}")
print(f"State objects: {len(state_objects)}")

if state_objects:
    first_state = list(state_objects.values())[0]
    print(f"First state: {first_state}")
else:
    print("No state objects found.")
