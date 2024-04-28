#!/usr/bin/python3
"""
Retrieves the number of each objects by type"""

from flask import jsonify
from models import storage
from api.v1.views import app_views

Object_types = {
            "Amenity": "amenities",
            "City": "cities",
            "Place": "places",
            "Review": "reviews",
            "State": "states",
            "User": "users"
        }

@app_views.route('/status', methods=['GET'])
def status():
    '''method that routes to status page and returns the status'''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def stats():
    '''method that returns the count of all objects by type'''
    num_of_obj_type = {}
    for key in object_types:
        num_of_obj_type[key] = storage.count(object_types[key])
    return jsonify(num_of_obj_type)
