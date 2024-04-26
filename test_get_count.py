#!/usr/bin/python3
""" Test .get() and .count() methods
"""

from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.state import State


db_storage = DBStorage()
new_state = State()
new_state.name = "Nairobi"
db_storage.new(new_state)
db_storage.save()

retrieved_state = db_storage.get(State, new_state.id)
print("Retrieved state:", retrieved_state)

state_count = db_storage.count(State)
print("Number of State objects:", state_count)

total_count = db_storage.count()
print("Total number of objects:", total_count)
