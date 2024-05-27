#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    Retrieves all User objects
    :return: JSON of all users
    """
    users = storage.all("User").values()
    return jsonify([user.to_json() for user in users])


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """
    Create user route
    :return: Newly created user object
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
def user_by_id(user_id):
    """
    Gets a specific User object by ID
    :param user_id: user object ID
    :return: User object with the specified ID or error
    """
    user = storage.get("User", user_id)

    if not user:
        abort(404)

    return jsonify(user.to_json())


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """
    Updates specific User object by ID
    :param user_id: user object ID
    :return: User object and 200 on success, or 400 or 404 on failure
    """
    user_json = request.get_json(silent=True)
    if not user_json:
        abort(400, 'Not a JSON')
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    for key, val in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user, key, val)
    user.save()
    return jsonify(user.to_json())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    Deletes User by ID
    :param user_id: user object ID
    :return: Empty dict with 200 or 404 if not found
    """
    user = storage.get("User", user_id)

    if not user:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})
