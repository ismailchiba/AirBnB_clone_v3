#!/usr/bin/python3
""" index file for the project """


from api.v1.views import app_views
from flask import jsonify
<<<<<<< HEAD
from models import storage, amenity, city, place, review, state, user


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Gets the counts in Json """
    counts = {
        "amenities": storage.count("Amenity"),
        "cities":  storage.count("City"),
        "places":  storage.count("Place"),
        "reviews": storage.count("Review"),
        "states":  storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(counts)
