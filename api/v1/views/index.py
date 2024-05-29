#!/usr/bin/python3
"""Defines the index view functions for the API.

This module provides endpoints for retrieving basic information about
the API and its current state. It offers two functionalities:

* `GET /status`: Returns a simple JSON response with a status key set
  to 'OK' to indicate the API is up and running.
* `GET /stats`: Returns a JSON object containing the number of stored
  objects for each model type (amenities, cities, places, reviews,
  states, users). It retrieves object counts from the storage layer.
"""
from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status')
def get_status():
    """Retrieves the API status.

    This function returns a JSON response with a status key set to 'OK',
    indicating that the API is operational.
    """
    return jsonify(status='OK')


@app_views.route('/stats')
def get_stats():
    """Retrieves statistics on the number of stored objects.

    This function iterates through a dictionary containing model classes
    mapped to their corresponding names. For each model type, it calls
    the `storage.count` method to retrieve the number of objects stored
    for that model. Finally, it returns a JSON object containing these
    counts.
    """
    objects = {
        'amenities': Amenity,
        'cities': City,
        'places': Place,
        'reviews': Review,
        'states': State,
        'users': User
    }
    for key, value in objects.items():
        objects[key] = storage.count(value)
    return jsonify(objects)
