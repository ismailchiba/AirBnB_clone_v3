#!/usr/bin/python3
"""
create Flask app, app_views
"""

from flask import jsonify, make_response, current_app
from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def api_status():
    """returns status Ok if working"""
    response = make_response(jsonify({'status': "OK"}), 200)
    return (response)


@app_views.route("/stats", strict_slashes=False)
def get_stats():
    """returns the stats of the api"""
    stat = {}
    obj_types = {
        'Amenity': "amenities",
        'City': "cities",
        'Place': "places",
        'Review': "reviews",
        'State': "states",
        'User': "users"
        }

    for obj in obj_types.keys():
        stat[obj_types[obj]] = storage.count(obj)

    return jsonify(stat), 200
