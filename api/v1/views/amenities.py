#!/usr/bin/python3
""" This module is to handle routes related to the amenities
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.amenity import Amenity


@app_views.route(
        "/amenities",
        methods=['GET'],
        strict_slashes=False)
def retrive_all_amenities():
    """ This function return list of all amenities """
    return jsonify([obj.to_dict() for _, obj in storage.all(Amenity).items()])


@app_views.route(
        "/amenities/<amenity_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_amenity(amenity_id):
    """ This function is used to retrive a specific amenity
        object using its id
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route(
        "/amenities/<amenity_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_amenity(amenity_id):
    """ This function is used to delete an amenity object when
        the DELETE method is called
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        "/amenities",
        methods=['POST'],
        strict_slashes=False)
def create_amenity():
    """ This function creates a new amenity object
    """
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_amenity = Amenity()
    new_amenity.name = request_data.get('name')
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        "/amenities/<amenity_id>",
        methods=['PUT'],
        strict_slashes=False)
def update_amenity(amenity_id):
    """ This function updates an existing amenity object
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    try:
        request_data = request.get_json()
    except Exception:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
