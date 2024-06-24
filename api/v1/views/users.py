#!/usr/bin/python3
"""A new view for Users objects
that handles all default RESTFul API actions"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def users_obj():
    """Retrieve an object into a valid JSON"""
    obj_users = storage.all(User).values()
    if obj_users is None:
        abort(404)

    all_users = []
    for user_obj in obj_users:
        all_users.append(user_obj.to_dict())
    return jsonify(all_users)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def user_obj_id(user_id):
    """Retrieve a user by ID"""
    obj_users = storage.get(User, user_id)
    if obj_users is None:
        abort(404)
    return jsonify(obj_users.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def user_delete(user_id):
    """Delete a user by ID"""
    obj_users = storage.get(User, user_id)
    if obj_users is None:
        abort(404)
    storage.delete(obj_users)
    storage.save()
    return jsonify({}), 200


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_post():
    """Create a new user"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "email" not in data:
        return jsonify({"error": "Missing email"}), 400
    if "password" not in data:
        return jsonify({"error": "Missing password"}), 400
    new_user = User(**data)
    new_user.save()

    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """Update user by ID"""
    obj_users = storage.get(User, user_id)
    if obj_users is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj_users, key, value)
    storage.save()
    return jsonify(obj_users.to_dict()), 200
