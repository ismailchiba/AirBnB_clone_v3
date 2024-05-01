#!/usr/bin/python3

""" This module sets blueprint for app"""

from api.v1.views import app_views, jsonify
from flask import Flask
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.user import User
from models import storage

app = Flask(__name__)


@app_views.route('/status')
def status():
    """ Get the status of the code"""
    """ get status"""
    stats = {"status": "OK"}
    return jsonify(stats)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """an endpoint that retrieves the number of each objects by type"""
    classes = [Amenity, City, Place, Review, State, User]
    names = ["amenities", "cities", "places", "reviews", "states", "users"]

    types_dic = {}
    number_types = 6
    for i in range(number_types):
        types_dic[names[i]] = storage.count(classes[i])

    return jsonify(types_dic)
