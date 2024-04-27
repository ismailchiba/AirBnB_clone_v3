#!/usr/bin/python3
"""
A module for users
"""
from api.v1.views import (app_views, User, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_user(user_id=None):
    """
    Retrieves a list of all users or of one specified by user_id
    """
    if user_id is None:
        user_list = [state.to_json() for state
                     in storage.all("User").values()]
        return jsonify(user_list)
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    return jsonify(user_obj.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    """
    Deletes a user based on the user_id
    """
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    storage.delete(user_obj)
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """
    Creates a user.
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if 'email' not in res.keys():
        return "Missing email", 400
    if 'password' not in res.keys():
        return "Missing password", 400
    new_user = User(**res)
    new_user.save()
    return jsonify(new_user.to_json()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    """
    Updates a user based on the JSON body
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    user_obj = storage.get("User", user_id)
    if user_obj is None:
        abort(404)
    for item in ("id", "email", "created_at", "updated_at"):
        res.pop(item, None)
    for key, value in res.items():
        setattr(user_obj, key, value)
    user_obj.save()
    return jsonify(user_obj.to_json()), 200
