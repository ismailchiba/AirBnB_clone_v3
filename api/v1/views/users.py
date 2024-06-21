#!/usr/bin/python3
"""Module for user-related API endpoints."""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """Retrieve a list of all users."""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieve a single user by its ID.

    Args:
        user_id (str): The ID of the user to retrieve.

    Returns:
        A JSON representation of the user, or a 404 error if not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """Delete a single user by its ID.

    Args:
        user_id (str): The ID of the user to delete.

    Returns:
        An empty JSON response with a 200 status code,
        or a 404 error if not found.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a new user.

    The request must contain a JSON object with 'email' and 'password' keys.

    Returns:
        A JSON representation of the newly created user,
        with a 201 status code.
    """
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'email' not in request_data:
        abort(400, "Missing email")
    if 'password' not in request_data:
        abort(400, "Missing password")
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Update a single user by its ID.

    Args:
        user_id (str): The ID of the user to update.

    Returns:
        A JSON representation of the updated user, with a 200 status code.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
