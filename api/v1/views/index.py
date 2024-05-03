#!/usr/bin/python3
""" Index module """
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON response"""
    return {"status": "OK"}


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """Returns object counts"""
    from models import storage
    states = storage.count('State')
    amenities = storage.count('Amenity')
    cities = storage.count('City')
    places = storage.count('Place')
    reviews = storage.count('Review')
    users = storage.count('User')
    return {
        "amenities": amenities,
        "cities": cities,
        "places": places,
        "reviews": reviews,
        "states": states,
        "users": users
    }
