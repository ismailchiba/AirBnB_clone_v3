#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
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


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Return the status of the API.

    This function returns a JSON response indicating the status of the API.

    Returns:
        response (flask.Response): A JSON response with the status of the API.
    """
    response = jsonify({"status": "OK"})
    response.status_code = 200
    return response


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Return the number of each object type by type.

    This function retrieves the count of each object type
    (states, cities, amenities, places, reviews, users)
    from the storage and returns the count in a JSON format.

    Returns:
        response (flask.Response): A JSON response containing
        the count of each object type.
    """
    cls_list = {
        State: "states",
        City: "cities",
        Amenity: "amenities",
        Place: "places",
        Review: "reviews",
        User: "users",
    }

    data = {name: storage.count(cls) for cls, name in cls_list.items()}
    response = jsonify(data)
    response.status_code = 200
    return response
