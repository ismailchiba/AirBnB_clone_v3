#!/usr/bin/python3
"""
Create a new view for Amenity objects that handles all default
RESTFul API actions
"""
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage, amenity


@app_views.rout('/amenities', methods=['GET'])
def get_amenities():
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amrnity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def amenity_uodate(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            ststtr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())


@app_views,route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return jsonify({})
