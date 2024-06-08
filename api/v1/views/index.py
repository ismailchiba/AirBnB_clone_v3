#!/usr/bin/python3
"""
Creating my flask app
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status')
def status():
    '''returns a JSON: "status": "OK"'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    '''endpoint that retrieves the number of each objects by type:'''
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('States'),
        'users': storage.count('User'),
    }
    return jsonify(stats)
