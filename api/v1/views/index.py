#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status")
def status_ok():
    """
    Return: status: OK
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def get_count():
    classes = {
        "amenity": Amenity,
        "city": City,
        "place": Place,
        "review": Review,
        "state": State,
        "user": User,
    }
    obj_count = {}

    for key, value in classes.items():
        obj_count[key] = storage.count(value)
    return jsonify(obj_count)
