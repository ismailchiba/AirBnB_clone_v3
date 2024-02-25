#!/usr/bin/python3
"""index"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


classes = {"users": "User", "places": "Place", "states": "State",
               "cities": "City", "amenities": "Amenity",
               "reviews": "Review"}


@app_views.route('/status', strict_slashes=False)
def status():
    """status route"""
    response = {
        "status": "OK"
    }

    return jsonify(response)


@app_views.route('/api/v1/stats', strict_slashes=False)
def stats():
    """stats route"""
    counts = {}
    for key, value in classes.items():
        counts[key] = storage.count(value)
    return jsonify(counts)
