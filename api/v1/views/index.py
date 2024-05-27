#!/usr/bin/python3
""" Returns a JSON response """


from flask import jsonify
from api.v1.views import app_views
from models import storage

# define the rute /status on the app_views Blueprint
@app_views.route('/status')
def get_status():
    # Return a JSON response with
    """ Returns the no of each object by type """
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'])
def object_stats():
    """Retrieves the no of each object by type"""
    objects = {
            "amenities": storage.count('Amenity'),
            "cities": storage.count('City'),
            "places": storage.count('Place'),
            "reviews": storage.count('Review'),
            "states": storage.count('State'),
            "users": storage.count('User'),
            }
    return jsonify(objects)
