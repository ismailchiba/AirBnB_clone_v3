#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Amenities"""
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_amenity():
    """Retrieves the list of all Amenity objects"""
    all_amenities = storage.all(Amenity).values()
    list_amenity = []
    for amenity in all_amenities:
        list_amenity.append(amenity.to_dict())
    return jsonify(list_amenity)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity_id(amenity_id):
    """Retrieves a Amenity by id"""
    amenity = storage.get(amenity, amenity_id)
    if not amenity:
        abort(404)

    return jsonify(amenity.to_dict())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity_id(amenity_id):
    """Deletes an Amenity object by id"""
    amenity = storage.get(amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """Creates an Amenity"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.json():
        """if not name in request.json()"""
        abort(400, "Missing name")

    amenity = request.json()
    instance = Amenity(**amenity)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(amenity), 201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(amenity, amenity_id):
        abort(404)

    amenity = storage.get(amenity, amenity_id)
    amenity_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in amenity_data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    storage.save()

    return make_response(jsonify(amenity.to_dict()), 200)
