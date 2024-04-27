#!/usr/bin/python3
"""
INDEX
"""
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.review import Review
from models.user import User
from api.v1.views import app_views
from flask import jsonify
from models import storage

classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews":Review,
    "states": State,
    "users": User
}


@app_views.route("/status", strict_slashes=False)
def getStatus():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def getObjects():
    objects = {}
    for key, value in classes.items():
        objects[key] = storage.count(value)
    return jsonify(objects)


if __name__ == "__main__":
    pass
