#!/usr/bin/python3
"""
index
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage

@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """
    status route
    :return: response with json
    """
    return jsonify({"status": "OK"}), 200

@app_views.route("/stats", methods=['GET'], strict_slashes=False)
def stats():
    """
    stats of all objs route
    :return: json of all objs
    """
    obj_types = ["Amenity", "City", "Place", "Review", "State", "User"]
    data = {}

    for obj_type in obj_types:
        count = storage.count(obj_type)
        data[obj_type.lower() + "s"] = count

    return jsonify(data), 200
