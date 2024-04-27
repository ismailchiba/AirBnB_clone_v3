#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.state import State
from models.city import City

city = City(state_id = "99f4e9c6-603c-4040-90b2-3054ca1906d9", name = "Lagos")
storage.new(city)
storage.save()
print("All objects: {}".format(storage.count()))
print("State objects: {}".format(storage.count(State)))

first_state_id = list(storage.all(State).values())[0].id
print("First state: {}".format(storage.get(State, first_state_id)))

