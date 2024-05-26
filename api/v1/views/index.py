#!/usr/bin/python3
"""index"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """Return a JSON response containing the number of objects by type."""
    from models import storage
    counts = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    }
    return jsonify(count)
