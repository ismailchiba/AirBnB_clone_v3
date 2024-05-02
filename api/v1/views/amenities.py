#!/usr/bin/python3

"""
This handles all the RESTFul API actions
(CRUD operations)
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/amenities', strict_slashes=False)
def get_amenities():
    """
    Retrieves the list of all Amenitiy
    objects
    """

    all_amenities = storage.all("Amenity")
    amenities = []
    for value in all_amenities.values():
        amenities.append(value.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieves an Amenity object given an amenity_id
    """

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Deletes an Amenity object  with the given amenity_id
    """

    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response({}, 200)


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Creates Amenity object and returns a dictionary
    of the created object
    """

    if not request.is_json:
        abort(400, description="Not a JSON")
    request_body = request.get_json()
    if 'name' not in request_body:
        abort(400, description='Missing name')
    amenity = Amenity(**request_body)
    storage.new(amenity)
    storage.save()
    return make_response(amenity.to_dict(), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Updates a Amenity object with the given amenity_id
    """
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    request_body = request.get_json()
    if not request.is_json:
        abort(400, description="Not a JSON")
    for key, value in request_body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return make_response(amenity.to_dict(), 200)
