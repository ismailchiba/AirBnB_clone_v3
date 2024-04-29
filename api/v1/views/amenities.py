#!/usr/bin/python3
"""return JSON """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def get_amenities():
    amenity_api = []
    amenities = storage.all(State).values()
    for amenity in amenities:
        amenity_api.append(amenity.to_dict())
    return jsonify(amenity_api)


@app_views.route('/amenities/<amenity_id>', methods=['GET'], strict_slashes=False)
def get_amenity_by_id(amenity_id):
    amenity = storage.get(State, amenity_id)
    if amenity:
        amenity_api = amenity.to_dict()
        return jsonify(amenity_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_by_id(amenity_id):
    amenity = storage.get(State, amenity_id)
    if amenity:
        storage.delete(amenity)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def put_amenity_by_id(amenity_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    amenity = storage.get(State, amenity_id)
    if amenity:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(amenity, k, v)
                storage.save()
        return jsonify(amenity.to_dict()), 201
    else:
        abort(404)
