#!/usr/bin/python3
""" index file for the project """


from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    """ Gets the counts in Json """
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
