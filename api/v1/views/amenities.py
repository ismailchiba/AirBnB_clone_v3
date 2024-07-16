#!/usr/bin/python3
"""this file adds HTTP methods for the Amenities class"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenity_list():
    """Retrieves the list of all Amenity objects"""
    amenities_data = storage.all(Amenity).values()
    amenities = []
    
    for amenity in amenities_data:
        amenities.append(amenity.to_dict())
    return jsonify(amenities)

@app_views.route('/amenities/<amenity_id>',
                methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Gets amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())

@app_views.route('/amenities/<amenity_id>',
                methods=['DELETE'], strict_slashes=False)
def del_amenity(amenity_id):
    """Deletes amenity by ID"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates an amenity"""
    data = request.get_json()
    if 'name' not in data:
        abort(400, description='Missing name')
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201

@app_views.route('/amenities/<amenity_id>',
                methods=['PUT'], strict_slashes=False)
def put_amenity(amenity_id):
    """Updates an amenity"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(400, description='Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return (jsonify(amenity.to_dict()), 200)

if __name__ == "__main__":
    app_views.run(debug=True)
