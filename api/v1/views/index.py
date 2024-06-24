#!/usr/bin/python3
"""Status of my API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', strict_slashes=False)
def status():
    """ Shows http status """
    return jsonify({"status": "ok"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ Shows number of ech class"""
    amenities = storage.count('Amenitie')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    states = storage.count('State')
    users = storage.count('User')
    return jsonify({"amenities": amenities, "cities": cities,
                    "places": places, "reviews": reviews,
                    "states": states, "users": users})
