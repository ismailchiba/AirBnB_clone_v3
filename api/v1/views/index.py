#!/usr/bin/python3
"""
Return the status of your API
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('/status')
def show_status():
    """
    returns a JSON: "status": "OK"
    """
    return (jsonify({"status": "OK"}))


@app_views.route('stats')
def count_obj():
    """retrieveis the number of each objects"""
    data = jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "states": storage.count(State),
        "users": storage.count(User)
        })
    return (data)
