#!/usr/bin/python3
"""
Module that handles all default RESTful API actions for Amenities class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """retrieves all amenity objects"""
    amenities = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in amenities]

    return jsonify(amenity_list)


@app_views.route("/amenities/<id>", methods=["GET"], strict_slashes=False)
def get_amenity(id):
    """retrieves a single amenity object by its id"""
    amenity = storage.get(Amenity, id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        abort(404)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """creates a new Amenity object"""
    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    if body.get("name") is None:
        abort(400, "Missing name")

    new_amenity = Amenity(**body)
    storage.new(new_amenity)
    storage.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<id>", methods=["PUT"], strict_slashes=False)
def update_amenity(id):
    """updates an Amenity object"""
    amenity = storage.get(Amenity, id)

    if amenity is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    excluded_keys = ["id", "created_at", "updated_at"]

    for key, value in body.items():
        if key not in excluded_keys:
            setattr(amenity, key, value)

    storage.save()

    return jsonify(amenity.to_dict()), 200


@app_views.route("/amenities/<id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(id):
    """deletes an Amenity object"""
    amenity = storage.get(Amenity, id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
