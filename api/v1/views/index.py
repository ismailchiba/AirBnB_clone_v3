#!/usr/bin/python3
""" This model handels the view routes
"""
from api.v1.views import app_views
from flask import jsonify
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route("/status", strict_slashes=False)
def status():
    """ This function returns the status of my API
    """
    return jsonify({"status": "OK"})


@app_views.route('stats', strict_slashes=False)
def number_of_objects():
    """ This function return the number of each object
    """
    result = {}
    objects = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    for key, obj in objects.items():
        result[key] = storage.count(obj)

    return result
