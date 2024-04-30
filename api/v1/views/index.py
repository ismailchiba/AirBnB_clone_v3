#!/usr/bin/python3
"""The index of the api"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''returns a JSON: "status": "OK" '''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def get_stats():
    """ Retrieves the number of each objects by type """
    classes = [Amenity, City, Place, Review, State, User]
    type_names = ["amenities", "city", "place", "reviews", "state", "user"]

    counts = {}
    for i, cls in enumerate(classes):
        counts[type_names[i]] = storage.count(cls)

    return jsonify(counts)
