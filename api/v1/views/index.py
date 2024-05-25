#!/usr/bin/python3
"""Index Module"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """Return a response status"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stat():
    """retrieves the number of each objects by type """
    return jsonify(
            amenities=storage.count("Amenity"),
            cities=storage.count("City"),
            places=storage.count("Place"),
            reviews=storage.count("Reviews"),
            states=storage.count("State"),
            users=storage.count("User")
            )
