#!/usr/bin/python3
"""Handles all default RESTFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity

@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_all_amenities():
    """Retrieves the list of all Amenity objects"""
    amenity_list = storage.all(Amenity).values()
    list_of_amenities = []
    for amenity in amenity_list:
        list_of_amenities.append(amenity.to_dict())
    return jsonify(list_of_amenities)


@app_views.route('/amenities/<amenities_id>/', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves a specific amenity by id"""

    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an amenity by id"""

    amenity = storage.get(Amenity, amenity_id)

    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()

    return jsonify({}), 200


@app_views.route('/amenities/<amenity_id>/amenities', methods=['POST'],
                 strict_slashes=False)
def post_amenity(amenity_id):
    """
    Creates an Amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    post_data = request.get_json()
    if not post_data:
        abort(400, description="Not a JSON")
    if 'name' not in post_data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**post_data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
    Updates an Amenity
    """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'amenity_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(amenity, key, value)
    storage.save()
    return jsonify(amenity.to_dict()), 200
