#!/usr/bin/python3
"""
A module for amenities
"""
from api.v1.views import (app_views, Amenity, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def view_amenity(amenity_id=None):
    """
    Retrieves a list of all amenties or of one specified by id
    """
    if amenity_id is None:
        all_amenities = [state.to_json() for state
                         in storage.all("Amenity").values()]
        return jsonify(all_amenities)
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    return jsonify(amenity_dict.to_json())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id=None):
    """
    Deletes a review based on the amenity_id
    """
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    storage.delete(amenity_dict)
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """
    Creates an amenity based on amenity_id
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if 'name' not in res.keys():
        return "Missing name", 400
    new_obj = Amenity(**res)
    new_obj.save()
    return jsonify(new_obj.to_json()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(amenity_id=None):
    """
    Updates an amenity based on it's id.
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    amenity_dict = storage.get("Amenity", amenity_id)
    if amenity_dict is None:
        abort(404)
    for item in ("id", "created_at", "updated_at"):
        res.pop(item, None)
    for key, value in res.items():
        setattr(amenity_dict, key, value)
    amenity_dict.save()
    return jsonify(amenity_dict.to_json()), 200
