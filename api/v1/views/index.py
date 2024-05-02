#!/usr/bin/python3
"""
creating a rout that returns a JSON
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", method=['GET'])
def status():
    return jsonify({"status": "OK"})


@app_views.route("/status", method=['GET'])
def all_state():
    class_object = {
        "amenities": storage.count("Amenities"),
        "cities": storage.count("Cities"),
        "places": storage.count("Places"),
        "reviews": storage.count("Review"),
        "states": storage.count("States"),
        "users": storage.count("Users")
    }
    return jsonify(class_object)
