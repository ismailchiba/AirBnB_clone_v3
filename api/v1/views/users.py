#!/usr/bin/python3
"""REST API routes for User objects"""


from models.user import User
from flask import jsonify, abort, request
from models import storage
from api.v1.views import app_views


# GET REQUEST


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def read_users():
    """ This reads the user objects"""
    all_users = [users.to_dict() for users in storage.all(User).values()]
    return jsonify(all_users)


# GET REQUEST


@app_views.route('/users/<user_id>', methods=['GET'])
def read_user(user_id):
    """ This retrieves a user object from users"""
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    return jsonify(user_obj.to_dict())


# DELETE REQUEST


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id):
    """ This deletes a user """
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    storage.delete(user_id)
    storage.save()
    return jsonify({}), 200


# CREATE REQUEST


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """ This route creates an object"""
    if not request.get_json():
        abort(400, description="Not a JASON")

    http_to_dict = request.get_json()

    if 'email' not in http_to_dict:
        abort(400, description="Missing email")

    if 'password' not in http_to_dict:
        abort(400, description="Missing password")

    new_user = User(**http_to_dict)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


# PUT REQUEST


@app_views.route('/users/<user_id>', methods=["PUT"])
def update_user(user_id):
    """ Update the user """
    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    http_to_dict = request.get_json()
    for key, value in http_to_dict.items():
        if key not in ['id', 'emails', 'created_at', 'updated_at']:
            setattr(user_obj, key, value)

    storage.save()
    return jsonify(user_obj.to_dict()), 200
