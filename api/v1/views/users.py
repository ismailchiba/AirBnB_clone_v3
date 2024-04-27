#!/usr/bin/python3
'''Handles User objects for RESTful API actions'''

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/users', methods=['GET', 'POST'], strict_slashes=False)
def all_users():
    '''gets and creates objects of User object'''
    if request.method == 'GET':
        all_users = storage.all(User)
        users = [obj.to_dict() for obj in all_users.values()]
        return jsonify(users)
    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'email' not in body:
            abort(400, 'Missing email')
        if 'password' not in body:
            abort(400, 'Missing password')
        new_user = User(**body)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['GET', 'DELETE', 'PUT'],
                    strict_slashes=False)
def users_by_id(user_id):
    '''gets, deletes, and updates objects of User object'''
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())
    if request.method == 'DELETE':
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        for key in body.keys():
            if key not in ['id', 'email', 'created_at', 'updated_at']:
                setattr(user, key, body[key])
        storage.save()
        return jsonify(user.to_dict()), 200
