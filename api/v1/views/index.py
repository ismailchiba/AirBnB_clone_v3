#!/usr/bin/python3
"""Index for Route Module"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models import Amenity, City, Place, Review, State, User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """ Returns the status of the API """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def obj_count():
    """Returns the number of each object type in the storage"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    count_obj = {}
    for i in range(len(classes)):
        count_obj[names[i]] = storage.count(classes[i])

    return jsonify(count_obj)
