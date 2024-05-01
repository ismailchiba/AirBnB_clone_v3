#!/usr/bin/python3
"""Amenity view module"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def retrive_amnety():
    """Retrieves the list of all Amenity objects"""
    all_amenities = [x.to_dict() for x in storage.all('Amenity').values()]
    if not all_amenities:
        return jsonify({})
    return jsonify(all_amenities)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['GET'])
def get_amnty(amenity_id):
    """Retrieves a Amenity object by id"""
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    return jsonify(amnty.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['DELETE'])
def del_amnty(amenity_id):
    """Deletes a Amenity object by id"""
    amnty = storage.get(Amenity, amenity_id)
    if amnty:
        amnty.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amnty():
    """Creates a Amenity object"""
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'name' not in response:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    obj = Amenity(**response)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 strict_slashes=False, methods=['PUT'])
def update_amnty(amenity_id):
    """Updates a Amenity object"""
    if not amenity_id:
        abort(404)
    amnty = storage.get(Amenity, amenity_id)
    if not amnty:
        abort(404)
    response = request.get_json(silent=True)
    if not response:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for k, v in dict(response).items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(amnty, k, v)
    storage.save()
    return jsonify(amnty.to_dict())
