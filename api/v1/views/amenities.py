#!/usr/bin/python3
"""amenities.py"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def amenity_get_all():
    """Retrieves all Amenity objects"""
    amenities = []
    amenity = storage.all("Amenity")
    for obj in amenity.values():
        amenities.append(obj.to_json())

    return jsonify(amenities)


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def amenity_create():
    """Create a new amenity """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')

    amenity = Amenity(**data)
    amenity.save()
    response = jsonify(amenity.to_json())
    response.status_code = 201
    return response


@app_views.route("/amenities/<amenity_id>",  methods=["GET"],
                 strict_slashes=False)
def amenity_by_id(amenity_id):
    """Retrieves a specific Amenity object by ID"""
    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["PUT"],
                 strict_slashes=False)
def amenity_put(amenity_id):
    """Updates specific Amenity object by ID"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, val)
    amenity.save()
    return jsonify(amenity.to_json())


@app_views.route("/amenities/<amenity_id>",  methods=["DELETE"],
                 strict_slashes=False)
def amenity_delete_by_id(amenity_id):
    """Deletes Amenity by id"""
    amenity = storage.get("Amenity", str(amenity_id))
    if amenity is None:
        abort(404)

    storage.delete(amenity)
    storage.save()
    return jsonify({})
