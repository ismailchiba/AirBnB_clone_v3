#!/usr/bin/python3
"""
Module for Endpoints for views of each class
Return the status of your API
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/status')
def show_status():
    """
    returns a JSON: "status": "OK"
    """
    return (jsonify({"status": "OK"}))


@app_views.route('stats')
def count_obj():
    """
    retrieves the number of each objects using count
    """
    """retrieveis the number of each objects"""
    data = jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
        "reviews": storage.count(Review),
        "states": storage.count(State),
        "users": storage.count(User)
        })
    return (data)
