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


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    state_api = []
    reviews = storage.all(State).values()
    for state in reviews:
        state_api.append(state.to_dict())
    return jsonify(state_api)


@app_views.route('/reviews/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state:
        state_api = state.to_dict()
        return jsonify(state_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/reviews/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def post_state_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state_by_id(state_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(state, k, v)
                storage.save()
        return jsonify(state.to_dict()), 201
    else:
        abort(404)
