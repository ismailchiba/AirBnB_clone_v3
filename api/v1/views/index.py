#!/usr/bin/python3
"""
This module contains the status route
"""
from flask import jsonify
import json
from . import app_views
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def get_status():
    """
    Return the status of the API
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def get_stats():
    """
    Return the number of objects by type
    """
    total_objects = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }

    return json.dumps(total_objects, indent=2)
