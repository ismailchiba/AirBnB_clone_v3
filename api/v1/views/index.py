#!/usr/bin/python3
<<<<<<< HEAD
"""
This module contains endpoint(route) status
"""
from api.v1.views import app_views
from flask import jsonify
=======
"""index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
>>>>>>> 6e6b784f8744e0630b80c062bbc68f66cf7ade6b
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = {"users": "User", "places": "Place", "states": "State",
           "cities": "City", "amenities": "Amenity",
           "reviews": "Review"}

<<<<<<< HEAD
@app_views.route('/stats', strict_slashes=False)
def status():
    """
    Returns a JSON status
    """
    return jsonify({"stats": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """
    Retrieves the number of each objects by type
    """
    return jsonify({"amenities": storage.count("Amenity"),
                    "cities": storage.count("City"),
                    "places": storage.count("Place"),
                    "reviews": storage.count("Review"),
                    "states": storage.count("State"),
                    "users": storage.count("User")})
=======

@app_views.route('/status', methods=['GET'])
def status():
    ''' routes to status page '''
    return jsonify({'status': 'OK'})


@app_views.route('/stats', methods=['GET'])
def count():
    '''retrieves the number of each objects by type'''
    count_dict = {}
    for cls in classes:
        count_dict[cls] = storage.count(classes[cls])
    return jsonify(count_dict)
>>>>>>> 6e6b784f8744e0630b80c062bbc68f66cf7ade6b
