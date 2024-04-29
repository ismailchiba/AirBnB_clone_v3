#!/usr/bin/python3
"""A Module for the index file"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """A fn that retrieves the number of each object by type"""

    classes = {
        "Amenity": storage.count("Amenity"),
        "City": storage.count("City"),
        "Place": storage.count("Place"),
        "Review": storage.count("Review"),
        "State": storage.count("State"),
        "User": storage.count("User")
    }
    return jsonify(classes)


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """A fn thst get status of the API"""

    return jsonify({"status": "OK"})
