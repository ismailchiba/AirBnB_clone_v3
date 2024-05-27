#!/usr/bin/python3
"""
route for handling User objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.user import User


@app_views.route("/users", methods=["GET"], strict_slashes=False)
def user_get_all():
    """
    retrieves all User objects
    """
    user_list = []
    user_object = storage.all("User")
    for obj in user_object.values():
        user_list.append(obj.to_json())

    return jsonify(user_list)


@app_views.route("/users", methods=["POST"], strict_slashes=False)
def create_user():
    """
    create user route
    """
    user_json = request.get_json(silent=True)
    if user_json is None:
        abort(400, 'Not a JSON')
    if "email" not in user_json:
        abort(400, 'Missing email')
    if "password" not in user_json:
        abort(400, 'Missing password')

    new_user = User(**user_json)
    new_user.save()
    response = jsonify(new_user.to_json())
    response.status_code = 201

    return response


@app_views.route("/users/<user_id>",  methods=["GET"], strict_slashes=False)
def user_by_id(user_id):
    """
    gets a specific User object by ID
    """

    fetched_object = storage.get("User", str(user_id))

    if fetched_object is None:
        abort(404)

    return jsonify(fetched_object.to_json())


@app_views.route("/users/<user_id>",  methods=["PUT"], strict_slashes=False)
def userUpdate_by_id(user_id):
    """
    updates specific User object by ID
    """
    user_json = request.get_json(silent=True)

    if user_json is None:
        abort(400, 'Not a JSON')

    fetched_object = storage.get("User", str(user_id))

    if fetched_object is None:
        abort(404)

    for key, value in user_json.items():
        if key not in ["id", "created_at", "updated_at", "email"]:
            setattr(fetched_object, key, value)

    fetched_object.save()

    return jsonify(fetched_object.to_json())


@app_views.route("/users/<user_id>",  methods=["DELETE"], strict_slashes=False)
def user_delete_by_id(user_id):
    """
    deletes User by id
    """

    fetched_object = storage.get("User", str(user_id))

    if fetched_object is None:
        abort(404)

    storage.delete(fetched_object)
    storage.save()

    return jsonify({})
