#!/usr/bin/python3
"""
all objects in storage
"""
import models
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/status', methods=['GET'])
def isItOk():
    """return its JSON data"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def all_objects():
    """return all objects in storage engine"""
    all_dict = {
             'amenities': storage.count(Amenity),
             'cities': storage.count(City),
             'places': storage.count(Place),
             'reviews': storage.count(Review),
             'states': storage.count(State),
             'users': storage.count(User)
           }
    return (jsonify(all_dict))
