#!/usr/bin/python3

"""This  module will create a flask app that serves the content of the AirBnB clone v3 RESTful API.
Create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
It will be imported in the app.py module
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """This function
    returns the status of the API
    It will be called when the route /status is requested
    """
    return jsonify(status="OK")


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stat():
    """
    This function
    retrieves the number of each object by type
    It will be called when the route /stats is requested
    """
    return jsonify(
        amenities=storage.count('Amenity'),
        cities=storage.count('City'),
        places=storage.count('Place'),
        reviews=storage.count('Review'),
        states=storage.count('State'),
        users=storage.count('User')
    )
