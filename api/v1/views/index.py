#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage


""" status and stats routes"""


classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


@app_views.route("/status")
def status():
    """ status code """

    return jsonify({"status": "OK"}), 200


@app_views.route("/stats")
def stats():
    """ object stats """

    obj_stats = {}
    for cls in classes:
        obj_stats[cls] = len(storage.all(classes[cls]))
    return jsonify(obj_stats), 200
