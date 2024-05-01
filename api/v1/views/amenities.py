#!/usr/bin/python3
""" this area is for file description"""
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def ret_amenity():
    """ Retrieves the list of all Amenity objects"""
    all_amenity = storage.all(Amenity).values()
    new_amenity = [i.to_dict() for i in all_amenity()]
    return jsonify(new_amenity)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenity_byid(amenity_id):
    """ Retrieves a Amenity object using id"""
    amn = storage.get(Amenity, amenity_id)
    if amn is None:
        abort(404)
    return jsonify(amn.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def rm_amenity(amenity_id):
    """ Deletes a Amenity object"""
    all_amenity = storage.get(Amenity, amenity_id)
    if all_amenity is None:
        abort(404)
    storage.delete(all_amenity)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def add_amenity():
    """ add or create amenity"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_amenity = Amenity(**request.get_json())
    new_amenity.save()
    return make_response(jsonify(new_amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def am_update(amenity_id):
    """ update Aminety object"""

    all_amenity = storage.get(Amenity, amenity_id)

    if all_amenity is None:
        abort(404)

    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(all_amenity, key, value)
    all_amenity.save()
    return make_response(jsonify(all_amenity.to_dict()), 200)
