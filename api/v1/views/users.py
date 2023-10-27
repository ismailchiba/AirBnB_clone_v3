#!/usr/bin/python3
"""API endpoints for users"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.user import User
from models import storage


@app_views.route('/users',
                 methods=['GET'],
                 strict_slashes=False)
def all_users():
    """Retrieve all users"""
    return jsonify(list(map(
        lambda x: x.to_dict(), storage.all(User).values()
    )))


@app_views.route('/users/<user_id>',
                 methods=["GET"],
                 strict_slashes=False)
def get_user(user_id):
    """Retrieves a particular user"""
    user = storage.get(User, user_id)
    return jsonify(user.to_dict()) if user else abort(404)


@app_views.route(
    "/users/<user_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def delete_user(user_id):
    """Deletes a particular user"""
    user = storage.get(User, user_id)
    if user:
        storage.delete(user)
        storage.save()
        return {}, 200
    return abort(404)


@app_views.route(
    '/users',
    methods=["POST"],
    strict_slashes=False
)
def post_user():
    """Creates a new user"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    if 'email' not in data:
        abort(400, "Missing email")

    if 'password' not in data:
        abort(400, "Missing password")
    new_user = User(**data)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=["PUT"],
    strict_slashes=False
)
def update_user(user_id):
    """Updates a user"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    ignore = (
        'id',
        'created_at',
        'updated_at',
        'email'
    )
    for key, value in data.items():
        if key not in ignore:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 201
