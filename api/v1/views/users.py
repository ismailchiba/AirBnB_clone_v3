#!/usr/bin/python3

"""This module will create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
it is the users view module
What it does is that it retrieves the list of all User objects
"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """This function
    Retrieves the list of all User objects
    It will be called when the route /users is requested
    And will return a JSON object with all User objects
    """
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """This function
    Retrieves a User object
    It will be called when the route /users/<user_id> is requested
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """This function
    Deletes a User object
    It will be called when the route /users/<user_id> is requested
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """This function
    Creates a User object
    it will be called when the route /users is requested with the POST method
    """
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if 'email' not in new_user:
        abort(400, "Missing email")
    if 'password' not in new_user:
        abort(400, 'Missing password')

    obj = User(**new_user)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def put_user(user_id):
    """This function
    Updates a User object
    This will be called when the route /users/<user_id> is requested with the PUT method
    And will return a JSON object with the updated User object
    """
    obj = storage.get(User, user_id)
    if not obj:
        """This function
        abort with 404 status code if obj is None
        It will be called when the route /users/<user_id> is requested
        """
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
