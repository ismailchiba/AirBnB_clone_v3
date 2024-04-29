#!/usr/bin/python3
"""return JSON """
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """status of an API"""
    stat = {'status': 'OK'}
    return jsonify(stat)


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def stats():
    """all states"""
    objs_num = {"states": storage.count(State), "cities": storage.count(City),
                "reviews": storage.count(Review), "users": storage.count(User),
                "places": storage.count(Place),
                "amenities": storage.count(Amenity)}
    return jsonify(objs_num)
