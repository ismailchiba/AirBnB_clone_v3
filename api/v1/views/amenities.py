#!/usr/bin/python3
""" Views for amenity object """

from flask import abort, request, jsonify, make_response
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    """ Get all amenities """
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ Get a amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ delete a amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """ Create a amenity """
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'name' not in response:
        abort(400, 'Missing name')
    new_amenity = Amenity(**response)
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """ Update a amenity """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    keys = ['id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in keys:
            setattr(amenity, key, value)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
