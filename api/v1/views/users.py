#!/usr/bin/python3
""" This module handles the users routes
"""
from flask import Blueprint, jsonify, abort, request
from werkzeug.exceptions import BadRequest
from models import storage
from models.user import User

app_users = Blueprint("app_users", __name__)


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_users.route("/", methods=['GET'])
def retrive_all_users():
    """ This function return list of all users """
    return [obj.to_dict() for _, obj in storage.all(User).items()]


@app_users.route("/<user_id>", methods=['GET'])
def retrive_user(user_id):
    """ This function is used to retrive a specific user
        object using its id
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    return user.to_dict()


@app_users.route("/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ This function is used to delete an user object when
        the DELETE method is called
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return {}, 200


@app_users.route("/", methods=['POST'])
def create_user():
    """ This function creates a new user object
    """
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'email' not in request_data:
        abort(400, description="Missing email")
    if 'password' not in request_data:
        abort(400, description="Missing password")

    new_user = User()
    new_user.email = request_data.get('email')
    new_user.password = request_data.get('password')
    new_user.save()
    return new_user.to_dict(), 201


@app_users.route("/<user_id>", methods=['PUT'])
def update_user(user_id):
    """ This function updates an existing user object
    """
    user = get_object_by_id(User, user_id)
    if not user:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(user, key, value)
    user.save()
    return user.to_dict(), 200
