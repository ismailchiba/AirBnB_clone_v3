#!/usr/bin/python3
"""Module for th enew view of Amenity objects"""

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import jsonify, abort, request


@app_views.route('/api/v1/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity)
                                                         .values()]
    return jsonify(amenities)


@app_views.route('/api/v1/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenities_by_id(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes the amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new amenity"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """Updates the amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict()), 200
