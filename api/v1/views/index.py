#!/usr/bin/python3
"""index View"""
from flask import jsonify
from api.v1.views import app_views
import models
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", strict_slashes=False)
def status_ok():
    """Returns Status OK"""
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def count_obj():
    """Counts Objects per Type"""
    counts = {
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
    }
    return jsonify(counts)
