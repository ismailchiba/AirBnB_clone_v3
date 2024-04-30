#!/usr/bin/python3
"""
routing app views status
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    """status OK"""
    return jsonify({"status": "OK"})


@app_views.route('stats')
def obj_count():
    """retrives the number of objects by type"""
    classes = {
        'Amenity': storage.count('Amenity'),
        'City': storage.count('City'),
        'Place': storage.count('Place'),
        'Review': storage.count('Review'),
        'State': storage.count('State'),
        'User': storage.count('User')
    }
    return jsonify(classes)
