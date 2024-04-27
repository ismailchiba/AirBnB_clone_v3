#!/usr/bin/python3
"""
Tihs file uses the created Blueprint to define routes
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
import json


@app_views.route('/status', strict_slashes=False)
def home():
    """
    returns a status ok
    """
    json_data = json.dumps({"status": "OK"}, indent=4)
    return jsonify(json_data)

@app_views.route('/stats')
def objects_count():
    """
    This retrieves the number of each object by type
    """

    stats = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Reviews"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }

    stats = json.dumps(stats, indent=4)

    return jsonify(stats)
