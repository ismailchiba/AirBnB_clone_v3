#!/usr/bin/python3
""" Module for status"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.city import City
from flask import jsonify


@app_views.route("/status", methods=["GET"])
def status():
    """returns status"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"])
def stats():
    """
    Retrieves the number of each objects by type
    returns stats
    """
    return jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User),
    })
