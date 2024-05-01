#!/usr/bin/python3
"""Amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities',
    methods=['GET'],
    strict_slashes=False
)
def get_amenities():
    """get all amenities"""
    all_amenity = []
    for amenity in storage.all('Amenity').values():
        all_amenity.append(amenity.to_dict())
    return jsonify(all_amenity)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_amenity(amenity_id):
    """get amenity from id"""
    try:
        i = storage.get('Amenity', amenity_id)
        return jsonify(i.to_dict())
    except Exception:
        abort(404)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    """delete amenity from id"""
    try:
        amenity = storage.get('Amenity', amenity_id)
        storate.delete(amenity)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False
)
def create_amenity():
    """create amenity"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """update amenity"""
    amenity = storage.get('Amenity', amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())
