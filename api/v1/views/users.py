#!/usr/bin/python3
"""Modle handles all default RESTful API actions for User objects"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves the list of all User objects"""
    users = storage.all(User)
    list_of_users = [user.to_dict() for user in users.values()]
    return jsonify(list_of_users), 200


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(user_id):
    """Retrieves an User object using the id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(user_id):
    """Deletes an User object from storage"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates an User object"""
    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    if 'email' not in json_data:
        abort(400, description='Missing email')
    if 'password' not in json_data:
        abort(400, description='Missing password')

    user = User(**json_data)

    storage.new(user)
    storage.save()

    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_amenity(user_id):
    """Update an User object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    json_data = request.get_json()
    for key, value in json_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
