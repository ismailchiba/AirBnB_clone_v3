#!/usr/bin/python3
"""
Create Flask app; app_views
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route('/sratus')
def api_status():
    """

    """
    response = {'status': "OK"}
    return jasonify(response)

@app_view.route('/status')
def get_status():
    """
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User'),
    }

    return jsonify(stats)
