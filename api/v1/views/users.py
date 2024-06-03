#!/usr/bin/python3
""" users views  GET/POST/DELETE and PUT HTTP method for users"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.user import User
from models import storage


@app_views.route("/users/")
@app_views.route("/users")
def get_users():
    """ return list of users"""

    users_dict = []
    for user in storage.all(User).values():
        users_dict.append(user.to_dict())
    return jsonify(users_dict), 200


@app_views.route("/users/<user_id>")
@app_views.route("/users/<user_id>/")
def get_user(user_id):
    """ get specific user"""

    for user in storage.all(User).values():
        if user.id == user_id:
            return jsonify(user.to_dict()), 200
    abort(404)


@app_views.route("/users/<user_id>", methods=['DELETE'])
@app_views.route("/users/<user_id>/", methods=['DELETE'])
def delete_user(user_id):
    """ delete user provided ID"""

    for user in storage.all(User).values():
        if user.id == user_id:
            storage.delete(usr)
            storage.save()
            return jsonify({}), 200
    abort(404)


@app_views.route("/users", methods=['POST'])
@app_views.route("/users/", methods=['POST'])
def create_user():
    """ create user object"""

    create_info = request.get_json()
    if create_info is None:
        abort(400, "NOT a JSON")
    if "email" not in create_info.keys():
        abort(400, "Missing email")
    if "password" not in create_info.keys():
        abort(400, "Missing password")

    new_user = User(**create_info)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route("/users/<user_id>", methods=["PUT"])
@app_views.route("/users/<user_id>/", methods=["PUT"])
def user_update(user_id):
    """ update user """

    skip_keys = ["id", "email", "created_at", "updated_at"]
    for user in storage.all(User).values():
        if user.id == user_id:
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            user_dict = user.to_dict()
            storage.delete(user)
            for key, value in update_info.items():
                if key not in skip_keys:
                    user_dict[key] = value
            updated_user = User(**user_dict)
            storage.new(updated_user)
            storage.save()
            return jsonify(user_dict), 200
    abort(404)
