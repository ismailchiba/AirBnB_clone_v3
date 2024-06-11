#!/usr/bin/python3
""" Test .get() and .count() methods
"""
import sys
from models import storage
from models.state import State
import time

print(sys.executable)
print(sys.path)

try:
    import MySQLdb
    print("MySQLdb is installed successfully!")
except ImportError as e:
    print("MySQLdb is not installed: {e}")

print("all objects ", storage.all())
print("state objects ", storage.all(State))
states = list(storage.all(State).values())
print(":state objects list: ", states)

if states:
        first_state_id = states[0].id
        print("first state ID: ", first_state_id)
else:
    print("No states objects available")
    time.sleep(1)
    print("Bye!")
"""print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))"""