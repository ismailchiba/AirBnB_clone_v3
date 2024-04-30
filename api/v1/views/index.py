#!/usr/bin/python3
"""create flask app"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


classes = {
           "amenities" : "Amenity",
           "cities": "City",
           "places": "Place",
           "reviews": "Review",
           "states": "State",
           "users": "User"
           }


@app_views.route('/status', methods=['GET'])
def app_return():
    """returns a JSON"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    """retrives the number of each objects by type"""
    storage = Storage()
    obj_counts = {}
    for obj_type in storage.types():
        obj_counts[obj_type] = storage.count(obj_type)
    return jsonify(obj_counts)
