#!/usr/bin/python3
"""index"""


from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {
    "users": "User",
    "places": "Place",
    "states": "State",
    "cities": "City",
    "amenities": "Amenity",
    "reviews": "Review"
}


@app_views.route('/status', strict_slashes=False)
def status():
    """status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """count"""
    dictionary = {}
    for cls in classes:
        dictionary[cls] = storage.count(classes[cls])
    return jsonify(dictionary)
