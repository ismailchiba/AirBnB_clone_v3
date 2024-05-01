#!/usr/bin/python3
"""
<<<<<<< HEAD
Create Flask app; app_views
"""
from flask import jsonify
=======
App views for AirBnB_clone_v3
"""

from flask import jsonify
from models import storage
>>>>>>> 1593e7d10c0cbd3ea850573dd62c4fc0d4305895
from api.v1.views import app_views


@app_views.route('/status')
<<<<<<< HEAD
def api_status():
    """

    """
    response = {'status': "OK"}
    return jsonify(response)
=======
def status():
    """ returns status """
    status = {"status": "OK"}
    return jsonify(status)

@app_views.route('/stats')
def count():
    """ returns number of each objects by type """
    total = {}
    classes = {"Amenity": "amenities",
               "City": "cities",
               "Place": "places",
               "Review": "reviews",
               "State": "states",
               "User": "users"}
    for cls in classes:
        count = storage.count(cls)
        total[classes.get(cls)] = count
    return jsonify(total)
>>>>>>> 1593e7d10c0cbd3ea850573dd62c4fc0d4305895
