#!/usr/bin/python3
"""
amenties objects that handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from models.amenity import Amenity
from api.v1.views import app_views
from models import storage


@app_views.route('/amenities', strict_slashes=False)
def get_all_amenity():
    """Get amenities instances"""
    amenity = storage.all(Amenity).items()
    lst_amenity = []
    for k, v in amenity:
        lst_amenity.append(v.to_dict())
    return jsonify(lst_amenity)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def get_amenity(amenity_id):
    """getting amenity using given id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        return jsonify(amenity.to_dict())
    else:
        return abort(404)


@app_views.route('/amenitis/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """deleting a amenity using id"""
    amenity = storage.get(Amenity, amenity_id)

    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """creating an amenity"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return (400, 'Not a JSON')
    element = request.get_json()

    if 'name' not in element:
        abort(400, "Missing name")

    amenity = Amenity(**element)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """updating anemities """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    if not request.get_json():
        return abort(400, 'Not a JSON')
    amenity_data = request.get_json()
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        not_key = ['id', 'created_at', 'updated_at']
        for k, v in amenity_data.items():
            if k not in not_key:
                setattr(amenity, k, v)
            amenity.save()
            return jsonify(amenity.to_dict()), 200
        else:
            return abort(404)
