#!/usr/bin/python3
"""Contains status, stats routes"""
from flask import jsonify
from api.v1.views import app_views
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
classes = {"users": User, "places": Place, "states": State,
           "cities": City, "amenities": Amenity,
           "reviews": Review}


@app_views.route('/status')
def status():
    """returns status of API"""
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
