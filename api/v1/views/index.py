#!/usr/bin/python3
"""Module for the index of blueprint"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {"users": User, "places": Place, "states": State,
           "cities": City, "amenities": Amenity,
           "reviews": Review}


# creating a route /status on the object app_views that returns a JSON
@app_views.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"}), 200


# Create an endpoint that retrieves the number of each objects by type
@app_views.route("/stats", methods=["GET"])
def stats():
    """Retrieves the number of each objects by type"""
    counts = {}

    for k, v in classes.items():
        count = storage.count(v)
        counts[k] = count
    return jsonify(counts), 200
