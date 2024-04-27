#!/usr/bin/python3
"""
Index model holds the endpoint (route)
"""
from api.v1.views import app_views, storage
from flask import jsonify


@app_views.route('/status/')
def status():
    """
    Returns the current status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats/')
def stats():
    """
    Returns a number of objects of each class
    """
    models_available = {"User": "users",
                        "Amenity": "amenities", "City": "cities",
                        "Place": "places", "Review": "reviews",
                        "State": "states"}
    stats = {}
    for cls in models_available.keys():
        stats[models_available[cls]] = storage.count(cls)
    return jsonify(stats)
