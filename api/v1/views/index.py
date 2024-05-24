#!/usr/bin/python3

from flask import jsonify

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """Return status"""
    response = jsonify({"status": "OK"})
    response.status_code = 200

    return response


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """Return the number of each objects by type"""
    cls_list = {
        State: "states",
        City: "cities",
        Amenity: "amenities",
        Place: "places",
        Review: "reviews",
        User: "users",
    }

    data = {name: storage.count(cls) for cls, name in cls_list.items()}

    response = jsonify(data)
    response.status_code = 200

    return response
