#!/usr/bin/python3
"""Handles all default RESTFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_all_users():
    """Retrieves the list of all User objects"""
    user_list = storage.all(User).values()
    list_of_users = []
    for user in user_list:
        list_of_users.append(user.to_dict())
    return jsonify(list_of_users)


@app_views.route('/users/<user_id>/', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a specific user by id"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a user by id"""

    user = storage.get(User, user_id)

    if not user:
        abort(404)
    storage.delete(user)
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a user
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    data = request.get_json()
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a User"""

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
