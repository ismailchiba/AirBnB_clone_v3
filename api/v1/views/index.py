#!/usr/bin/python3
"""
created Flask app: app_views
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage


@app_views.route("/status", methods=['GET'])
def status():
    """
    status route
    :return: response with json
    """

    response = {'status': "OK"}
    return jsonify(response)
    # alternative
    # return jsonify({"status": "OK"})

# status route
@app_views.route("/stats")
def get_stats():
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