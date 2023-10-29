#!/usr/bin/python3 
"""THis is the index page view"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', strict_slashes=False)
def status():
    """This is the status of the api"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """Gets the stats of all objects"""
    obj = {
            'amenities': Amenity,
            'cities': City,
            'places': Place,
            'reviews': Review,
            'states': State,
            'users': User
            }
    for key, value in obj.items():
        obj[key] = storage.count(value)
    return jsonify(obj)
