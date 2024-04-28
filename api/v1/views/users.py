#!/usr/bin/python3
"""
    States view for the API.
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all User objects"""
    objs = storage.all(User)
    return jsonify([obj.to_dict() for obj in objs.values()])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user(user_id):
    """Retrieves a User object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_user(user_id):
    """Deletes a User object"""
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def add_user():
    """Returns the new user with the status code 201"""
    try:
        new_obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'email' not in new_obj:
        abort(400, "Missing email")
    if 'password' not in new_obj:
        abort(400, "Missing password")
    obj = User(**new_obj)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    obj = storage.get(User, user_id)
    if not obj:
        abort(404)

    try:
        req = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
