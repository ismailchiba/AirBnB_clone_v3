#!/usr/bin/python3
"""Script that create Flask application; app_views."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def api_status():
    """return jsonify"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def get_stats():
    """json stats"""
    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(stats)
