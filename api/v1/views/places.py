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


@app_views.route('/places', methods=['GET'], strict_slashes=False)
def get_places():
    place_api = []
    places = storage.all(State).values()
    for place in places:
        place_api.append(place.to_dict())
    return jsonify(place_api)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    place = storage.get(State, place_id)
    if place:
        place_api = place.to_dict()
        return jsonify(place_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place_by_id(place_id):
    place = storage.get(State, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places', methods=['POST'], strict_slashes=False)
def post_place_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place_by_id(place_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    place = storage.get(State, place_id)
    if place:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(place, k, v)
                storage.save()
        return jsonify(place.to_dict()), 201
    else:
        abort(404)
