#!/usr/bin/python3
"""Amenity functions"""

from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


@app_views.route(
    '/amenities',
    methods=['GET'],
    strict_slashes=False
)
def get_all_amenitie():
    """get all amenities"""
    all_amenity = []
    for x in storage.all(Amenity).values():
        all_amenity.append(x.to_dict())
    return jsonify(all_amenity)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_each_amenity(amenity_id):
    """get amenity from id"""
    x = storage.get(Amenity, amenity_id)
    if x is None:
        abort(404)
    return jsonify(x.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    """delete amenity from id"""
    x = storage.get(Amenity, amenity_id)
    if x is None:
        abort(404)
    storage.delete(x)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False
)
def create_amenity():
    """create amenity"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')
    i = Amenity(**data)
    i.save()
    return jsonify(i.to_dict()), 201


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """update amenity"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
