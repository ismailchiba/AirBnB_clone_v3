#!/usr/bin/python3
""" View for User object """

from flask import abort, make_response, request, jsonify
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_all_users():
    """ Retrieves all users """
    users = storage.all(User).values()
    list_users = []
    for user in users:
        list_users.append(user.to_dict())
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """ get a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ Deletes a user """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ Creates new user """
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'email' not in response:
        abort(400, 'Missing email')
    if 'password' not in response:
        abort(400, 'Missing password')
    new_user = User(**response)
    new_user.save()
    return make_response(jsonify(new_user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Update user's information """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in keys:
            setattr(user, key, value)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
