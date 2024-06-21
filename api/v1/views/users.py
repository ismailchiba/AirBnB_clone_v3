#!/usr/bin/python3
"""
city restful api
"""
from flask import jsonify
from flask import request
from flask import abort
from models.user import User
from models import storage
from api.v1.views import app_views


@app_views.route('/users/',
                 strict_slashes=False, methods=['GET'])
def get_all_users():
    """get all users"""
    users = storage.all(User)
    all_list = [user.to_dict() for user in users.values()]
    return jsonify(all_list)


@app_views.route('/users/<user_id>/',
                 strict_slashes=False, methods=['GET'])
def get_userById(user_id):
    """get User by user_id"""
    users = storage.all(User)
    for k, v in users.items():
        if v.to_dict().get('id') == user_id:
            return jsonify(v.to_dict())
    return (abort(404))


@app_views.route('/users/',
                 strict_slashes=False, methods=['POST'])
def create_user():
    """post a city for a certain state id"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    elif 'email' not in data.keys():
        return (abort(400, 'Missing email'))
    elif 'password' not in data.keys():
        return (abort(400, 'Missing password'))
    else:
        user = User(**data)
        storage.new(user)
        storage.save()
        return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>/',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """update city in state"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        abort(400, 'Not a JSON')
    user = storage.get(User, user_id)
    if user is None:
        return (abort(404))
    ignore = ['id', 'email', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(user, k, v)
    user.save()
    return jsonify(user.to_dict()), 200


@app_views.route('/users/<user_id>/',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """delete the city by its city id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200
