#!/usr/bin/python3
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', strict_slashes=False)
def get_users():
    """Retrieves the list of all User objects."""
    users = storage.all(User)
    user_list = []
    for user in users.values():
        user_list.append(user.to_dict())
    return jsonify(user_list)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['GET'])
def get_user(user_id):
    """Retrieves a User object."""
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_user(user_id):
    """Deletes a User object."""
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return jsonify({})


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a User."""
    user_json = request.get_json()
    if user_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'email' not in user_json:
        return make_response(jsonify({'error': 'Missing email'}), 400)
    if 'password' not in user_json:
        return make_response(jsonify({'error': 'Missing password'}), 400)
    user = User(**user_json)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>',
                 strict_slashes=False, methods=['PUT'])
def update_user(user_id):
    """Updates a User object."""
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user_json = request.get_json()
    if user_json is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in user_json.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict())
