#!/usr/bin/python3
'''View for Amenity objs that handles all default RESTFul API actions'''

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route("/amenities", methods=["GET"], strict_slashes=False)
def all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = storage.all(Amenity).values()
    amenities = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities)


@app_views.route("/amenities/<amenity_id>", methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a Amenity obj"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity = amenity.to_dict()
    return jsonify(amenity)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes anAmemenity Object"""
    emp_dict = {}
    amenity = storag.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify(emp_dict), 200


@app_views.route("/amenities", methods=["POST"], strict_slashes=False)
def post_amenity():
    """Create an Amenity"""
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 201


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates Amenity Objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    skeys = ["id", "created_at", "updated_at"]
    for key, value in data.items():
        if key not in skeys:
            setattr(amenity, key, value)
    amenity.save()
    amenity = amenity.to_dict()
    return jsonify(amenity), 200
