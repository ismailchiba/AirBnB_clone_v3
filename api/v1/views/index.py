#!/usr/bin/python3
"""
Create a route `/status` on the object app_views.
"""
# Import the required modules
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'])
def hbnbApi_status():
    """
    Returns a JSON response for RESTful API health.
    """
    response = {'status': 'OK'}
    return jsonify(response)


@app_views.route('/stats', methods=['GET'])
def getVerb_stats():
    """
    Retrieves the number of each objects by type.
    """
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)
