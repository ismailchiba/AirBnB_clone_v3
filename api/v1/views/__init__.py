#!/usr/bin/python3
""" A module that initialises the views model with a blueprint app_views"""
from flask import Blueprint
from models.amenity import Amenity
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review

classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


app_views = Blueprint('/api/vi', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
