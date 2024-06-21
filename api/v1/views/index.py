#!/usr/bin/python3
"""Defines a status route API."""
from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route("/status")
def status():
    """Returns the server"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """Retrives the count."""
    return jsonify({
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User")
    })
