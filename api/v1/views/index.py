#!/usr/bin/python3
""" api status """

from api.v1.views import app_views
from models import storage
from flask import jsonify
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State


@app_views.route('/status', strict_slashes=False)
def return_status():
    """ Return status """
    message = jsonify(status='OK')
    return message


@app_views.route('/stats', strict_slashes=False)
def object_by_type():
    """ Retrieves the number of object by type """
    objects = {"amenities": Amenity,
               "cities": City,
               "places": Place,
               "reviews": Review,
               "states": State,
               "users": User}
    for obj in objects:
        objects[obj] = storage.count(objects[obj])
    return jsonify(objects)
