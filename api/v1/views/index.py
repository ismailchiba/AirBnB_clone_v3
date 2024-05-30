#!/usr/bin/python3
"""
<<<<<<< HEAD
module to generate json response
"""

from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json

classes = {"amenities": Amenity, "cities": City,
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status', strict_slashes=False)
def index():
    response = {"status": "OK"}
    return jsonify(response)


# @app_views.route('/stats', strict_slashes=False)
# def stats():
#     response = {}
#     for key, value in classes.items():
#         response[key] = storage.count(value)
#     return jsonify(response)

@app_views.route('/stats')
def stats():
    """returns status : OK"""
    obj ={
        "amenities":storage.count(Amenity), 
        "cities": storage.count(City), 
        "places": storage.count(Place), 
        "reviews": storage.count(Review), 
        "states": storage.count(State), 
        "users": storage.count(User)
    }
    return jsonify(obj)
