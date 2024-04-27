#!/usr/bin/python3
"""This module defines routes for the status and statistics of the API."""

from models import storage
from flask import Flask
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', strict_slashes=False)
def status():
    """Returns the status of the API.

    Returns:
        JSON: A JSON object with the status "OK".
    """
    return jsonify({'status': 'OK'})


@app_views.route('/api/v1/stats')
def get_stats():
    """Returns statistics about the data stored in the API.

    Returns:
        JSON: A JSON object with counts of various data types stored in the API.
    """
    counts = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }

    return jsonify(counts)
