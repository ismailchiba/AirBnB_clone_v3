#!/usr/bin/python3

"""
This is the index module
It does the following:
- does a status check
- retrieves the number of each object by type
- returns the status of the API
- retrieves the number of each object by type
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    This function
    returns the status of the API
    in a JSON format
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """
    This function
    retrieves the number of each object by type
    It returns the number of each object by type
    """
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
