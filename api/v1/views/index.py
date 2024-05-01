#!/usr/bin/python3
"""
    This is the index page handler for Flask.
"""
from flask import Flask, make_response, jsonify
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}


@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
