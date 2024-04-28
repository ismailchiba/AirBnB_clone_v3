#!/usr/bin/python3
"""handle User operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def get_all_user():
    """retrieves all the list of user"""
    all_user = []
    user_obj = storage.all("User")
    for user in user_obj.values():
        all_user.append(user.to_json())
    return jsonify(all_user)


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def get_user_by_id(user_id):
    """get user using its specific id"""
    user_obj = storage.get("User", str(user_id))
    if user_obj is None:
        abort(404)

    return jsonify(user_obj.to_json())


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """create a new user"""
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    resp = jsonify(new_user.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def user_put(user_id):
    """updates specific User using its specific ID"""
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    user_obj = storage.get("User", str(user_id))
    if user_obj is None:
        abort(404)
    for key, value in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(user_obj, key, value)
    user_obj.save()

    return jsonify(user_obj.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def delete_user_by_id(user_id):
    """deletes User using its"""
    user_obj = storage.get("User", str(user_id))
    if user_obj is None:
        abort(404)

    storage.delete(user_obj)
    storage.save()
    return jsonify({})
