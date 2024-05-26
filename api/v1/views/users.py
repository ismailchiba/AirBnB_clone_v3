#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for User objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.user import User

api_route = "/users/<string:user_id>"


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_users():
    """
    Retrieves the list of all User objects
    """
    users_list = []
    users_obj = storage.all(User)

    for obj in users_obj.values():
        users_list.append(obj.to_dict())

    response = jsonify(users_list), 200

    return response


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    Create a new user.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new user and the HTTP status code 201.
    """
    body = request.get_json(silent=True)
    user_fields = ["email", "password"]

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for field in user_fields:
        if field not in body:
            message = "Missing {}".format(field)
            return make_response(jsonify({"error": message}), 400)

    new_user = User(**body)

    new_user.save()

    response = jsonify(new_user.to_dict()), 201

    return make_response(response)


@app_views.route(api_route, methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """
    Retrieve a specific user by its ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        tuple: A tuple containing the JSON representation of
        the user and the HTTP status code.

    Raises:
        404: If the user with the specified ID does not exist.
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    response = jsonify(user.to_dict()), 200

    return response


@app_views.route(api_route, methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """
    Delete a user by its ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the user with the specified ID does not exist.
    """
    user = storage.get(User, user_id)

    if user is None:
        abort(404)

    storage.delete(user)
    storage.save()

    return jsonify({})


@app_views.route(api_route, methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """
    Update a user by its ID.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated user and the HTTP status code 200.

    Raises:
        404: If the user with the specified ID does not exist.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    user = storage.get(User, str(user_id))

    if user is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(user, key, value)

    storage.save()

    response = jsonify(user.to_dict()), 200

    return response
