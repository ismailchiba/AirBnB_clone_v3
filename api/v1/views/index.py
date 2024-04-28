#!/usr/bin/python3
""" index file for the project """


from api.v1.views import app_views
from flask import jsonify
from models import storage, amenity, city, place, review, state, user


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def get_status():
    """Returns the status of the API."""
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats():
    """ retrieves the number of each object type """
    objects = {
            "amenities": storage.count(amenity.Amenity),
            "cities": storage.count(city.City),
            "places": storage.count(place.Place),
            "reviews": storage.count(review.Review),
            "states": storage.count(state.State),
            "users": storage.count(user.User),
            }
    return jsonify(objects)
