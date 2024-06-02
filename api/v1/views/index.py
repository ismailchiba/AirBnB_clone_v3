#!/usr/bin/python3
"""
Creating an endpoint that
retrieves the number of each objects by type
"""


from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """
    Returning the status of an API
        Checking the status 200 - OK
    """

    return jsonify({"status": "OK"}), 200


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """
    Retrieving the type of objects
        Storing all classes into a variable
    """
    classes = {"amenities": Amenity, "cities": City, "places": Place,
               "reviews": Review, "states": State, "users": User}
    stats = {}
    for class_name, cls in classes.items():
        stats[class_name] = storage.count(cls)
    return jsonify(stats)
