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


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    user_api = []
    users = storage.all(State).values()
    for user in users:
        user_api.append(user.to_dict())
    return jsonify(user_api)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    user = storage.get(State, user_id)
    if user:
        user_api = user.to_dict()
        return jsonify(user_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user_by_id(user_id):
    user = storage.get(State, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user_by_id(user_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    user = storage.get(State, user_id)
    if user:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(user, k, v)
                storage.save()
        return jsonify(user.to_dict()), 201
    else:
        abort(404)
