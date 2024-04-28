#!/usr/bin/python3
""" Containes views for users/ api end point """

from api.v1.views import app_views
from flask import jsonify, make_response, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'],
                 strict_slashes=False)
def get_users():
    """ returns a list of all users json """
    users = storage.all("User").values()
    list_users = [user.to_dict() for user in users]
    return jsonify(list_users)


@app_views.route('/users/<user_id>', methods=['GET'],
                 strict_slashes=False)
def get_user(user_id):
    """ returns json of a single user with an ide <iser_id> """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    else:
        return jsonify([user.to_dict()])


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """ deletes a user with an id <user_id> """
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    else:
        storage.delete(user)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """ Adds user """
    if request.is_json:
        kwargs_data = request.get_json()
        if 'email' not in kwargs_data:
            abort(400, description='Missing email')
        elif 'password' not in kwargs_data:
            abort(400, description='Missing password')
        else:
            user = User(**kwargs_data)
            user.save()
            return make_response(jsonify([user.to_dict()]), 201)
    abort(400, description='Not a JSON')


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def update_user(user_id):
    """ updates an amenity with an id <amenity_id> """
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    else:
        if request.is_json:
            kwargs_data = request.get_json()
            ignore = ['id', 'email', 'created_at', 'updated_at']
            for key, val in kwargs_data.items():
                if key not in ignore:
                    setattr(user, key, val)
            storage.save()
            return make_response(jsonify([user.to_dict()]), 200)
        abort(400, description='Not a JSON')
