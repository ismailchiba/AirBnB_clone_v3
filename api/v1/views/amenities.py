#!/usr/bin/python3
""" New view for Amenity objects that handles all default RESTFul API action"""

from flask import jsonify, request, abort
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', methods=['GET'])
def list_amenities():
    amenities = storage.all(Amenity).values()
    amenities_json = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_json), 200


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json), 200


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save()
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    storage.save()
    amenity_json = amenity.to_dict()
    return jsonify(amenity_json), 200
