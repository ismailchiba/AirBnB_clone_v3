#!/usr/bin/python3

"""
This module creates a new view for User objects
Create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
This view handles all default RestFul API actions.
"""

from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort, jsonify, make_response, request



@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """
    Retrieves the list of all User objects.
    Returns:
        JSON: A list of dictionaries representing User objects.
    """
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def single_user(user_id):
    """
    Retrieves a User object.
    Returns:
        JSON: A dictionary representing the User object.
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """
    Deletes a User object.
    Returns:
        JSON: An empty dictionary with the status code 200.
    """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """
    Creates a User object.
    Returns:
        JSON: A dictionary representing the new User object with the status code 201.
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
    """
    Updates a User object.
    Returns:
        JSON: A dictionary representing the updated User object with the status code 200.
    """
    obj = storage.get(User, user_id)
    if not obj:
        """abort with 404 status code if obj is None"""
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
