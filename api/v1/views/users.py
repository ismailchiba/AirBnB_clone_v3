#!/usr/bin/python3
"""users module"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_users():
    """get users"""
    users = []
    userObject = storage.all("User")
    for user in storage.all("User").values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def user_create():
    """create user"""
    newUser = request.get_json(silent=True)
    if newUser is None:
        abort(400, 'Not a JSON')
    if "email" not in newUser:
        abort(400, 'Missing email')
    if "password" not in newUser:
        abort(400, 'Missing password')
    new_user = User(**newUser)
    new_user.save()
    resp = jsonify(new_user.to_dict())
    resp.status_code = 201
    return resp


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """get user by id"""
    userObject = storage.get("User", str(user_id))
    if userObject is None:
        abort(404)
    return jsonify(userObject.to_dict())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """ put user by id"""
    newUser = request.get_json(silent=True)
    if newUser is None:
        abort(400, 'Not a JSON')
    userObject = storage.get("User", str(user_id))
    if userObject is None:
        abort(404)
    for key, val in newUser.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(userObject, key, val)
    userObject.save()
    return jsonify(userObject.to_dict())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """ delete user by id"""
    fetched_obj = storage.get("User", str(user_id))
    if fetched_obj is None:
        abort(404)
    storage.delete(fetched_obj)
    storage.save()
    return jsonify({})
