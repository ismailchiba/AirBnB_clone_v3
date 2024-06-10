#!/usr/bin/python3
"""Returns status ok"""

from api.v1.views import app_views
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

@app_views.route('/', methods=['GET'])
def status():
    """gets the status"""
    return jsonify({"status": "OK"})
