#!/usr/bin/python3
"""User"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User



@app_views.route('/users', methods=['GET'], strict_slashes=False)
def get_user():
    list_of_user = [obj.to_dict() for obj in storage.all(User).values()]
    return jsonify(list_of_user)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_users(user_id):
    """get user id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)

def delete_user(user_id):
    """delete user"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def create_user():
    """create user"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'email' not in request.get_json():
        return make_response(jsonify({"error": "Missing email"}), 400)
    if 'password' not in request.get_json():
        return make_response("error": "Missing password"}), 400)

    json = request.get_json()
    obj = User(**json)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def user_post(user_id):
    """user post"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    obj = storage.get(User, user_id)
    if obj is None:
        abort(404)
    for k, v in request.get_json().items():
        if k not in ['id', 'email', 'created_at', 'updated']:
            setattr(obj, k, v)
    storage.save()
    return jsonify(obj.to_dict())
