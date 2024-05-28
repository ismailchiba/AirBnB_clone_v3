#!/usr/bin/python3
"""Module that handles all default RESTful API actions for Users class"""

from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
    """retrieves all User objects"""
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
    """retrieves a User object by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create a new User with"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if "email" not in new_user:
        abort(400, "Missing email")
    if "password" not in new_user:
        abort(400, "Missing password")

    obj = User(**new_user)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """update a User object by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ["id", "email", "created_at", "updated_at"]:
            setattr(obj, key, value)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    """delete a User object by id"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)
