#!/usr/bin/python3
""" Index Module"""
from models import storage
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    return jsonify({"status": "OK"})


@app_views.route("/stats", strict_slashes=False)
def stats():
    class_dict = {"Amenity": "amenities", "City": "cities", "Place": "places",
                  "Review": "reviews", "State": "states", "User": "users"}
    objs = {class_dict[cls]: storage.count(cls) for cls in class_dict}
    return jsonify(objs)
