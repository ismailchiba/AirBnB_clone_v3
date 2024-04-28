#!/usr/bin/python3
"""
api status
"""
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
from api.v1.views import app_views


classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}

@app_views.route("/status")
def status():
    """Status of  API"""
    return jsonify({"status": "OK"})

@app_views.route("/stats")
def stats():
    """Retrieve the number of each object type"""
    statistics = {}

    try:
        for key, cls in classes.items():
            count = storage.count(cls)
            statistics[key] = count

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(statistics)
