#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
<<<<<<< HEAD
=======

>>>>>>> 8471f4eadde8806234297f3b75e7ad8d245a4f73
from models import storage


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
<<<<<<< HEAD

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
=======
    data = {
        "status": "OK"
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp


@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    data = {
        "amenities": storage.count("Amenity"),
        "cities": storage.count("City"),
        "places": storage.count("Place"),
        "reviews": storage.count("Review"),
        "states": storage.count("State"),
        "users": storage.count("User"),
    }

    resp = jsonify(data)
    resp.status_code = 200

    return resp
>>>>>>> 8471f4eadde8806234297f3b75e7ad8d245a4f73
