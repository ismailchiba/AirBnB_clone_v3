#!/usr/bin/python3
""" connects to API"""
from api.v1.views import app_views
from flask import jsonify
from models import storage, amenity, city, place, review, state, user


classes = [amenity.Amenity,
           city.City,
           place.Place,
           review.Review,
           state.State,
           user.User
           ]


@app_views.route('/status', strict_slashes=False)
def appStatus():
    """Creates a dictionary for response"""
    response = {
                "status": "OK"
            }
    return jsonify(response)


@app_views.route('/stats', strict_slashes=False)
def appStats():
    """ Retrieves the Stats of the app """
    stats = {}
    for cls in classes:
        class_name = cls.__name__
        count = storage.count(cls)
        stats[class_name] = count
    return jsonify(stats)
