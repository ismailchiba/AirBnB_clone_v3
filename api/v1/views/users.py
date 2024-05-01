#!/usr/bin/python3
"""view for User objects that handles all default
RESTFul API actions
"""
from flask import jsonify, abort, request
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """Retrieves the list of all Users objects"""
    user = storage.all(User).values()
    users_list = [user.to_dict() for user in user]
    return jsonify(users_list)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_a_user(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)

    if user:
        return jsonify(user.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a_user(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_a_user():
    """Creates a User"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    data = request.get_json()

    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user.id>', methods=['PUT'], strict_slashes=False)
def update_a_user(user_id):
    """Updates a User object"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict()), 200
    else:
        return abort(404)
