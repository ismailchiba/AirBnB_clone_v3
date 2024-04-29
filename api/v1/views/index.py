#!/usr/bin/python3
""" Module for status"""
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.state import State
from models.place import Place
from models.review import Review
from models.user import User
from models.city import City
from flask import jsonify


# Dictionary mapping model classes to their names
model_classes = {
    "amenities": Amenity,
    "cities": City,
    "places": Place,
    "reviews": Review,
    "states": State,
    "users": User,
}


@app_views.route("/status", methods=["GET"], strict_slashes=False)
def status():
    """
    Returns the status of the application.
    ---
    responses:
      200:
        description: Status of the application.
    """
    return jsonify({"status": "OK"})


@app_views.route("/stats", methods=["GET"], strict_slashes=False)
def stats():
    """
    Retrieves the number of each object by type.
    ---
    responses:
      200:
        description: Object count by type.
      500:
        description: Error occurred, unable to retrieve statistics.
    """
    stats = {
        cls_name: storage.count(cls) for cls_name, cls in model_classes.items()
    }
    return jsonify(stats)


@app_views.route("/nop", methods=["GET"])
def page_not_found():
    """
    Returns a 'Not Found' error response.
    ---
    responses:
      404:
        description: The requested resource was not found.
    """
    return jsonify({"error": "Not found"})
