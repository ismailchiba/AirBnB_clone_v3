#!/usr/bin/python3

"""
This is a view for User object that handles all default
RESTFul API actions (CRUD operations)
"""

from flask import abort, make_response, jsonify, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_all_users():
    """
    Retrieves  the list of all User objects
    """

    all_users = storage.all("User")

    user_obj = []

    for val in all_users.values():
        user_obj.append(val)

    return jsonify(user_obj)


@app_views.route('/users/<user_id>', strict_slashes=False)
def get_user(user_id):
    """
    Retrieves a User object  with the specified
    user_id
    """
    user = storage.get("User", user_id)

    if user is not None:
        return user.to_dict()

    abort(404)


@app_views.route('/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    This deletes a user object with the specified user_id
    """

    user = storage.get("user", user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return make_response({}, 200)


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a User object and returns the new user object
    """

    if not request.is_json:
        abort(400,  description='Not a JSON')

    request_body = request.get_json()

    if 'email' not in request_body:
        abort(400, description='Missing email')

    if 'password' not in request_body:
        abort(400, description='Missing password')

    new_user = User(**request_body)

    storage.new(new_user)
    storage.save()

    return make_response(new_user.to_dict(), 201)


@app_views.route('/users/<state_id>', methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates a User object with the specified state_id
    """

    user = storage.get("User", user_id)

    if user is not None:
        if not request.is_json:
            abort(404, description='Not a JSON')

        request_body = request.get_json()

        for key, val in request_body.items():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, val)

        user.save()
        return user.to_dict()

    abort(404)
