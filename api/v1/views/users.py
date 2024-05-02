#!/usr/bin/python3

"""Interact with the User model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.user import User
from models.base_model import BaseModel as BM


users = F(__name__)


@AV.route('/users', methods=['GET', 'POST'])
def get_or_create_users():
    """Get all users / Create a new user w no Id"""
    Users = storage.all('User')
    if Users is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
        response = [user.to_dict() for user in Users.values()]
        status = 200

    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('email') is None:
            abort(400, 'Missing email')
        if RQ_json.get('password') is None:
            abort(400, 'Missing password')

        new_user = User(**RQ_json)
        new_user.save()
        response = new_user.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_user(user_id=None):
    """Get, delete or update a User object w a given identifier"""
    response = {}
    user = storage.get('User', user_id)
    if user is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = user.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')

        user = User.db_update(RQ_json)
        user.save()   # type: ignore
        response = user.to_dict()   # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        user.delete()   # type: ignore
        del user
        status = 200
    return jsonify(response), status
