#!/usr/bin/python3
""" Test .get() and .count() methods
"""
from models import storage
from models.user import User

#print("All objects: {}".format(storage.count()))
#print("State objects: {}".format(storage.count(Place)))

#first_state_id = storage.get(Place, 'd3c7d891-8a80-444f-bd65-95f4e1fa616b')
#print("First state: {}".format(first_state_id))


#print("All objects: {}".format(storage.count()))
#print("State objects: {}".format(storage.count(Place)))

first_state_id = list(storage.all(User).values())[0].id
print("First User: {}".format(storage.get(User, first_state_id)))
