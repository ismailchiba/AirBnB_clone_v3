#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Users"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_user():
    """Retrieves the list of all User objects"""
    all_users = storage.all(user).values()
    list_user = []
    for user in all_users:
        list_user.append(user.to_dict())
    return jsonify(list_user)


@app_views.route("/users/<user_id>", methods=["GET"], strict_slashes=False)
def get_user_id(user_id):
    """Retrieves a User by id"""
    user = storage.get(user, user_id)
    if not user:
        abort(404)

    return jsonify(user.to_dict())


@app_views.route("/users/<user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user_id(user_id):
    """Deletes a User object by id"""
    user = storage.get(user, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.json():
        """if not name in request.json()"""
        abort(400, "Missing name")

    user = request.json()
    instance = User(**user)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(user), 201)


@app_views.route("/users/<user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    """Updates a User object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(user, user_id):
        abort(404)

    user = storage.get(user, user_id)
    user_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in user_data.items():
        if key not in ignore_keys:
            setattr(user, key, value)
    storage.save()

    return make_response(jsonify(user.to_dict()), 200)
