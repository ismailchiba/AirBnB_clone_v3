#!/usr/bin/python3

"""
This module creates a new view for User objects
It handles all default RestFul API actions
Create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    This function retrieves the status of the API
    returns the status of the API
    It returns a JSON: "status": "OK"
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """
    This function retrieves the number of each object by type
    retrieves the number of each object by type
    And returns a JSON object with the count of each object
    """
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
