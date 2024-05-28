#!/usr/bin/python3
"""index.py"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


classes = {
    "amenities": storage.count(Amenity),
    "cities": storage.count(City),
    "places": storage.count(Place),
    "reviews": storage.count(Review),
    "states": storage.count(State),
    "users": storage.count(User)
}


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def route():
    """Returns an OK status code in json format"""
    response = {
        "status": "OK"
    }

    return jsonify(response), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Retrieves the number of each objects by type"""
    stats_dict = {}
    for key, value in classes.items():
        stats_dict[key] = value

    return jsonify(stats_dict)
