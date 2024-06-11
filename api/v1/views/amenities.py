#!/usr/bin/python3
"""
Create a new view for Amenity objects
that handles all default RESTFul API actions
"""
from flask import Flask, jsonify, make_response, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
import json


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    all_amenity = storage.all(Amenity).values()
    amenity_list = [amenity.to_dict() for amenity in all_amenity]
    response = make_response(json.dumps(amenity_list, indent=2) + "\n")
    response.headers["Content-Type"] = "application/json"
    return response


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a State object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates a Amenity use POST request"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = Amenity(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def updata_state(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    data = request.get_json()
    for k, v in data.items():
        if k not in ["id", "created_at", "updated_at"]:
            setattr(amenity, k, v)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
