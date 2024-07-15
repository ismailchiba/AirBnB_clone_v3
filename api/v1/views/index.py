#!/usr/bin/python3
""" Defines a status route """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review,
           "states": State, "users": User}


@app_views.route("/status", strict_slashes=False)
def status():
    """
    returns OK status
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False, methods=['GET'])
def stats():
    """
    returns counts of different objects
    """
    stats_dict = {}
    for k, v in classes.items():
        stats_dict[k] = storage.count(v)
    return jsonify(stats_dict)
