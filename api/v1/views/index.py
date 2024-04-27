#!/usr/bin/python3
"""
This module contains the endpoint definitions for the AirBnB clone API.
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

classes_values = {
    "amenities": "Amenity",
    "cities": "City",
    "places": "Place",
    "reviews": "Review",
    "states": "State",
    "users": "User"
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def api_status():
    """
    Returns the status of the API as a JSON response.
    """
    return jsonify({"status": "OK"})


@app_views.route('/api/v1/stats', methods=['GET'], strict_slashes=False)
def api_stats():
    """
    Retrieves the number of each object type and returns as a JSON response.
    """
    obj_num = {}
    for key, value in classes_values.items():
        obj_num[key] = storage.count(value)
    return jsonify(obj_num)
