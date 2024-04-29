#!/usr/bin/python3

"""
This module contains the index view for the API
Create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
It is the main file that is executed to start the application.
"""
from api.v1.views import app_views
from models import storage
from flask import jsonify



@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    This function returns the status of the API
    returns the status of the API
    The status is a JSON object with the key "status" and the value "OK"
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """
    This returns the number of each object by type
    retrieves the number of each object by type
    it retrieves the number of each object by type
    """
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
    