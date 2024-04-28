#!/usr/bin/python3
"""User"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.user import User


@app_views.route(
    '/users',
    methods=['GET'],
    strict_slashes=False
)
def get_users():
    """get all users"""
    all_users = [i.to_dict() for i in storage.all(User).values()]
    return jsonify(all_users)


@app_views.route(
    '/users/<user_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_user(user_id):
    """get user from id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_user(user_id):
    """delete user from id"""
    i = storage.get(User, user_id)
    if i is None:
        abort(404)
    storage.delete(i)
    storage.save()
    return jsonify({})


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False
)
def create_user():
    """create user"""
    user = request.get_json()
    if not user:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in user:
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in user:
        return make_response(jsonify({"error": "Missing password"}), 400)
    i = User(**user)
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_user(user_id):
    """update user"""
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, k, v)
    storage.save()
    return jsonify(user.to_dict())
