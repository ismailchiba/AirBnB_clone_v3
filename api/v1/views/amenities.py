#!/usr/bin/python3
"""
This file contains views for the Amenity module
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET', 'POST'],
                 strict_slashes=False)
def get_or_post_amenities():
    """ get amenities all amenities """
    if request.method == 'GET':
        all_amenities = storage.all(Amenity)
        amenities = [obj.to_dict() for obj in all_amenities.values()]
        return make_response(jsonify(amenities), 200)

    elif request.method == 'POST':
        if not request.is_json or not request.get_json().get('name', None):
            abort(400)
        js = request.get_json()
        obj = Amenity(**js)
        obj.save()
        data = storage.get(Amenity, obj.id).to_dict()
        return make_response(jsonify(data), 201)

    elif request.method == 'HEAD':
        return make_response(jsonify(""), 200)


@app_views.route('/amenities/<amenity_id>', methods=['GET', 'PUT', 'DELETE'],
                 strict_slashes=False)
def get_or_update_amenity(amenity_id):
    """ gets or update amenity by id """
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(amenity.to_dict()), 200)

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400)
        for key, value in request.get_json().items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(amenity, key, value)
        storage.save()
        return jsonify(amenity.to_dict()), 200

    elif request.method == 'DELETE':
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)

    elif request.method == 'HEAD':
        return make_response(jsonify(""), 200)
