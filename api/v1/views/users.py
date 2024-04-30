#!/usr/bin/python3
""" Handle API functions for users"""
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/all_users.yml')
def fetch_users():
    """
    Retrieve the list of users
    """
    all_users = storage.all(User).values()
    users_list = []
    for user in all_users:
        users_list.append(user.to_dict())
    return jsonify(users_list)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/user/get_user.yml', methods=['GET'])
def fetch_user(user_id):
    """ Retrieve a user by ID """
    user = storage.get(User, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/user/delete_user.yml', methods=['DELETE'])
def remove_user(user_id):
    """
    Delete a user object
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
@swag_from('documentation/user/post_user.yml', methods=['POST'])
def create_user():
    """
    Create a new user
    """
    if not request.get_json():
        abort(400, description="Request is not in JSON format")

    if 'email' not in request.get_json():
        abort(400, description="Missing email")
    if 'password' not in request.get_json():
        abort(400, description="Missing password")

    user_data = request.get_json()
    new_user = User(**user_data)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/user/put_user.yml', methods=['PUT'])
def update_user(user_id):
    """
    Update a user
    """
    user = storage.get(User, user_id)

    if not user:
        abort(404)

    if not request.get_json():
        abort(400, description="Request is not in JSON format")

    ignore_fields = ['id', 'email', 'created_at', 'updated_at']

    user_data = request.get_json()
    for key, value in user_data.items():
        if key not in ignore_fields:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
