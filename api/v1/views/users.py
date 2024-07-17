#!/usr/bin/python3
"""this file adds HTTP methods for the User class"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Lists of all User"""
    users = storage.all(User).values()
    users_list = [user.to_dict() for user in users]
    return jsonify(users_list)

@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())

@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Deletes a User"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a User"""
    data = request.get_json(force=True)
    if not data:
        return abort(400, description='Not a JSON')
    if 'email' not in data:
        return abort(400, description='Missing email')
    if 'password' not in data:
        return abort(400, description='Missing password')
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return make_response(jsonify(new_user.to_dict()), 201)

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """Updates a User"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True)
    if not data:
        return abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200

if __name__ == '__main__':
    app_views.run(debug=True)
