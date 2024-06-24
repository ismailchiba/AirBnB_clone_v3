#!/usr/bin/python3
"""A new view for Amenity objects
that handles all default RESTFul API actions"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_obj():
    """Retrieve an object into a valid JSON"""
    obj_amenity = storage.all(Amenity).values()
    if obj_amenity is None:
        abort(404)

    all_amenities = []
    for ame_obj in obj_amenity:
        all_amenities.append(ame_obj.to_dict())
    return jsonify(all_amenities)


@app_views.route("/amenities/<amenity_id>",
                 methods=["GET"], strict_slashes=False)
def amenity_obj_id(amenity_id):
    """Retrieve an amenity object by ID """
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    return jsonify(obj_amenity.to_dict())


@app_views.route("/amenities/<amenity_id>",
                 methods=["DELETE"], strict_slashes=False)
def amenity_delete(amenity_id):
    """Delete a amenity by ID"""
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)
    storage.delete(obj_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_post():
    """Create a new amenity object"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_amenity = Amenity(**data)
    new_amenity.save()

    return jsonify(new_amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>",
                 methods=["PUT"], strict_slashes=False)
def amenity_put(amenity_id):
    """Update a amenity by ID"""
    obj_amenity = storage.get(Amenity, amenity_id)
    if obj_amenity is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj_amenity, key, value)
    storage.save()
    return jsonify(obj_amenity.to_dict()), 200
