#!/usr/bin/python3
"""The index of the api"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''returns a JSON: "status": "OK"'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """ retrieves the number of each objects by type"""
    objects = {
        'amenity': Amenity,
        'city': City,
        'place': Place,
        'reviews': Review,
        'state': State,
        'user': User
    }
    counts = {}
    for key, value in objects.items():
        counts[key] = storage.count(value)
        return jsonify(counts)
