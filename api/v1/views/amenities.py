#!/usr/bin/python3
"""
defines api for accessing amenity objects
"""
from flask import jsonify, abort, request
from . import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'])
@app_views.route('/amenities/', methods=['GET'])
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenities = storage.all(Amenity)
    if not amenities:
        abort(404)
    amenities = [amenity.to_dict() for amenity in amenities.values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity_obj(amenity_id):
    """Retrieves a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity_obj(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
@app_views.route('/amenities/', methods=['POST'])
def create_amenity_obj():
    """ Creates a amenity object"""
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    amenity = Amenity(**data)
    storage.new(amenity)
    storage.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """
    Updates an Amenity object
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    for key, val in data.items():
        if hasattr(amenity, key):
            setattr(amenity, key, val)
    storage.save()
    return jsonify(amenity.to_dict()), 200
