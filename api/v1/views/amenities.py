#!/usr/bin/python3
"""Amenity"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.amenity import Amenity


# @app_views.route(
#     '/amenities',
#     methods=['GET'],
#     strict_slashes=False
# )
# def get_amenities():
#     """get all amenities"""
#     all_amenity = [i.to_dict() for i in storage.all(Amenity).values()]
#     return jsonify(all_amenity)


# @app_views.route(
#     '/amenities/<amenity_id>',
#     methods=['GET'],
#     strict_slashes=False
# )
# def get_amenity(amenity_id):
#     """get amenity from id"""
#     amenity = storage.get(Amenity, amenity_id)
#     if amenity is None:
#         abort(404)
#     return jsonify(amenity.to_dict())


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_amenity(amenity_id):
    """delete amenity from id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/amenities',
    methods=['POST'],
    strict_slashes=False
)
def create_amenity():
    """create amenity"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)
    i = Amenity(**data)
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route(
    '/amenities/<amenity_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_amenity(amenity_id):
    """update amenity"""
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, k, v)
    storage.save()
    return jsonify(amenity.to_dict())
