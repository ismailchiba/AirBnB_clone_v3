#!/usr/bin/python3
"""Module for new view of the user object"""


from api.v1.views import app_views
from models import storage
from models.user import User
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieves all the users"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieves a user by id"""
    user = storage(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delets the user by id"""
    user = Storage.gat(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a new user"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    email = data.get('email')
    password = data.get('password')
    if not email:
        abort(400, 'Missing email')
    if not password:
        abort(400, 'Missing password')
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates the user object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict()), 200
