#!/usr/bin/python3
"""
<<<<<<< HEAD
Module for Endpoints for views of each class
=======
Return the status of your API
>>>>>>> 0c19be942c8d0bf9fd8e096729db5507a9554aae
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
<<<<<<< HEAD
from models.review import Review
=======
>>>>>>> 0c19be942c8d0bf9fd8e096729db5507a9554aae
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
<<<<<<< HEAD
    """
    retrieves the number of each objects using count
    """
=======
    """retrieveis the number of each objects"""
>>>>>>> 0c19be942c8d0bf9fd8e096729db5507a9554aae
    data = jsonify({
        "amenities": storage.count(Amenity),
        "cities": storage.count(City),
        "places": storage.count(Place),
<<<<<<< HEAD
        "reviews": storage.count(Review),
=======
>>>>>>> 0c19be942c8d0bf9fd8e096729db5507a9554aae
        "states": storage.count(State),
        "users": storage.count(User)
        })
    return (data)
