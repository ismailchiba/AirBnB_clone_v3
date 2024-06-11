#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
import time


storage.reload()

all_objects_count = storage.count()
state_objects_count = storage.count(State)

#sample first object 
first_state = list(storage.all(State).values())[0]

# Print the output
print("All objects:", all_objects_count)
print("State objects:", state_objects_count)
print("First state:", first_state)
print("waiting for the next execution of similar objects in a different  format!")
time.sleep(1)
print("wait a second!")
time.sleep(3)

# error handler for the MySQLdb existence(it had issues on my local machine, so dontr pay attention to thi snippe)
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