#!/usr/bin/python3
"""
Routes for handling User objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Retrieves all User objects.
    """
    user_list = [user.to_json() for user in storage.all("User").values()]
    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Creates a new User object.
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        abort(400, 'Not a JSON')

    if "email" not in user_json:
        abort(400, 'Missing email')

    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    return jsonify(new_user.to_json()), 201


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieves a specific User object by ID.
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_json())


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Updates a specific User object by ID.
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        abort(400, 'Not a JSON')

    user = storage.get("User", user_id)
    if not user:
        abort(404)

    for key, value in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, value)

    user.save()
    return jsonify(user.to_json())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Deletes a User object by ID.
    """
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    storage.delete(user)
    storage.save()
    return jsonify({}), 200
