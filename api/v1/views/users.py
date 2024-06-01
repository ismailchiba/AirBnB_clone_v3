#!/usr/bin/python3
"""
Handling RESTFUL API actions for User objects
"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_list():
    """
    Returning all User objects list
    in a json representation
    """

    users = storage.all(User)
    user_list = [user.to_dict() for user in users.values()]
    return jsonify(user_list), 200


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """
    User by its id is returned
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    return jsonify(user.to_dict()), 200


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
    Deleting one user with user's id
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    user.delete()
    storage.save()

    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creating new user
    """

    try:
        user_data = request.get_json()
        if user_data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    if 'email' not in user_data:
        abort(400, description="Missing email")
    if 'password' not in user_data:
        abort(400, description="Missing password")

    new_user = User(**user_data)
    storage.new(new_user)
    storage.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Function to update user
    """

    user = storage.get(User, user_id)

    if not user:
        abort(404)

    try:
        data = request.get_json()
        if data is None:
            abort(400, description="Not a JSON")
    except Exception as e:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, value)

    user.save()

    return jsonify(user.to_dict()), 200
