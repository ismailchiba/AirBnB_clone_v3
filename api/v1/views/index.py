#!/usr/bin/python3
"""index"""

from api.v1.views import app_views
from flask import jsonify
from models import storage

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """gets status in json format"""
    return jsonify({"status": "OK"})


@app_views.route('stats', methods=['GET'], strict_slashes=False)
def stats():
    """retrieves the number of each objects by type"""
    stats = {
            "amenities": storage.count("Amenity"),
            "cities": storage.count("Cities"),
            "places": storage.count("Place"),
            "reviews": storage.count("Review"),
            "states": storage.count("State"),
            "users": storage.count("User")
            }
    return jsonify(stats)
