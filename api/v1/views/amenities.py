#!/usr/bin/python3
"""
Routes for handling Amenity objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def get_all_amenities():
    """
    Retrieves all Amenity objects.
    """
    amenity_list = [amenity.to_json() for amenity in storage.all("Amenity").values()]
    return jsonify(amenity_list)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates a new Amenity object.
    """
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        abort(400, 'Not a JSON')

    if "name" not in amenity_json:
        abort(400, 'Missing name')

    new_amenity = Amenity(**amenity_json)
    new_amenity.save()
    return jsonify(new_amenity.to_json()), 201


@app_views.route("/amenities/<amenity_id>", methods=["GET"], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    """
    Retrieves a specific Amenity object by ID.
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["PUT"], strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a specific Amenity object by ID.
    """
    amenity_json = request.get_json(silent=True)
    if not amenity_json:
        abort(400, 'Not a JSON')

    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    for key, value in amenity_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)

    amenity.save()
    return jsonify(amenity.to_json())


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"], strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes a Amenity object by ID.
    """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200
