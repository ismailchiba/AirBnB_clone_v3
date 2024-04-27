#!/usr/bin/python3
"""Handles Amenity objects for RESTful API actions
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/amenities', methods=['GET', 'POST'], strict_slashes=False)
def all_amenities():
    """gets and creates objects of Amenities object"""
    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        amenities = [obj.to_dict() for obj in all_amenities.values()]
        return jsonify(amenities)

    if request.method == 'POST':
        amenity_dict = request.get_json()
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_amenity = Amenity(**amenity_dict)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def amenities_by_id(amenity_id):
    """gets, deletes, and updates objects of Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())

    if request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key, value in req_json.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200
