#!/usr/bin/python3
""" It creates a new view for User objects"""

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State, City
from flask import request


@app_views.route('/users', methods=['GET'] strict_slashes=False)
def retrieves_all_users():
    """It retrieves all users."""
    usersObject = storage.all('User')
    list = []
    for user in usersObject.values():
        list.append(user.to_dict())
    return jsonify(list)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_user():
    """It retrieves a user otherwise raises an error."""
    userObject = storage.get('User', 'user_id')
    if userObject is None:
        abort(404)
    return jsonify(userObject.to_dict()), 'OK'


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_user():
    """ It deletes a User otherwise raises an error."""
    userObject = storage.get('User', 'user_id')
    if userObject is None:
        abort(404)
    storage.delete(userObject)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users/', methods=['POST'],
                 strict_slashes=False)
def creates-user():
    """It creates a User."""

    response = request.get_json()

    if response is None:
        abort(400, {'Not a JSON'})
    if "email" not in response:
        abort(400, {'Missing email'})
    if "password" not in response:
        abort(400, {'Missing password'})

    userObject = User(__tablename__=response['__tablename__'])
    storage.new(userObject)
    storage.save()
    return jsonify(userObject.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_user():
    """It updates a User."""

    response = request.get_json()
    userObject = storage.get('User', 'user_id')

    if userObject is None:
        abort(404)
    if response is None:
        abort(400, {'Not a JSON'})
    ignoreKeys = ['id', 'email', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(userObject, key)
    storage.save()
    return jsonify(userObject.to_dict()), 200
