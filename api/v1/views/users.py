#!/usr/bin/python3
"""RESTFul API"""
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def list_all_users():
    """Retrieve the list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users]), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new User object"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'email' not in data:
        abort(400, description="Missing email")
    if 'password' not in data:
        abort(400, description="Missing password")
    new_user = User(**data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id):
    """Retrieve a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user_by_id(user_id):
    """Delete a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user_by_id(user_id):
    """Update a User object by user_id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'email', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
