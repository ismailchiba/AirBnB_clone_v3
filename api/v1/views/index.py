#!/usr/bin/python3
"""Index module for the API"""
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.user import User
from models.review import Review

from api.v1.views import app_views
# app_views.url_map.strict_slashes = False


@app_views.route('/status')
def status():
    """Return a JSON-formatted status response."""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def count_stats():
    """Return a JSON-formatted stats response."""
    stats = {
        "amenities": Amenity,
        "cities": City,
        "places": Place,
        "reviews": Review,
        "states": State,
        "users": User
    }

    count_stats = {
        key: storage.count(value) for key, value in stats.items()
    }
    return jsonify(count_stats)
