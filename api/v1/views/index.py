#!/usr/bin/python3
"""
API endpoints for status and statistics.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    Returns status OK.
    """
    data = {"status": "OK"}
    return jsonify(data), 200


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    Returns statistics of various objects.
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }
    return jsonify(data), 200
