#!/usr/bin/python3

"""
This module contains some utility functions for the API
"""

from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status_okay():
    """
    Returns Status OK code.
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def number_objects():
    """Returns number of objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    number_objects = {}
    for i in range(len(classes)):
        number_objects[names[i]] = storage.count(classes[i])

    return jsonify(number_objects)
