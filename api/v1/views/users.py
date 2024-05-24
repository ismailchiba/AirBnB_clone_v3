#!/usr/bin/python3
"""
defines api for accessing user objects
"""
from flask import jsonify, abort, request
from . import app_views
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'])
@app_views.route('/users/', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects
    """
    users = storage.all(User)
    if not users:
        abort(404)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user_obj(user_id):
    """Retrieves a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user_obj(user_id):
    """Deletes a User object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
@app_views.route('/users/', methods=['POST'])
def create_user_obj():
    """ Creates a user object"""
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")
    if "email" not in data:
        abort(400, "Missing email")
    if "password" not in data:
        abort(400, "Missing password")
    user = User(**data)
    storage.new(user)
    storage.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Updates an User object
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    for key, val in data.items():
        if hasattr(user, key):
            setattr(user, key, val)
    storage.save()
    return jsonify(user.to_dict()), 200
