#!/usr/bin/python3
""" index """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """ status """
    return {"status": "OK"}


@app_views.route('/stats')
def stats_each_objetc():
    """ retrieves the number of each objects by type """
    from models.state import State
    from models.city import City
    from models.user import User
    from models.amenity import Amenity
    from models.place import Place
    from models.review import Review

    c_am = storage.count(Amenity)
    c_ci = storage.count(City)
    c_pl = storage.count(Place)
    c_re = storage.count(Review)
    c_st = storage.count(State)
    c_us = storage.count(User)
    return jsonify(amenities=c_am, cities=c_ci, places=c_pl,
                   reviews=c_re, states=c_st, users=c_us)
