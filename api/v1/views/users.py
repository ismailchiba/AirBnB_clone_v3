#!/usr/bin/python3
"""
    Handles all default RESTFul API actions for User objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models import storage
from models.user import User


@app_views.route("/users", strict_slashes=False)
def get_users():
    """
        Retrieves all User objects
    """
    all_users = storage.all(User)
    user_list = list()
    for user in all_users.values():
        user_list.append(user.to_dict())
    return Response(json.dumps(user_list, indent=2),
                    mimetype="application/json", status=200)


@app_views.route("/users/<user_id>", strict_slashes=False,)
def get_user(user_id):
    """
        Retrieves a User object
    """
    all_users = storage.all(User)
    for user in all_users.values():
        if user_id == user.id:
            return Response(json.dumps(user.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)


@app_views.route("/users/<user_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_user(user_id):
    """
        Deletes a User object
    """
    keep_user = None
    all_users = storage.all(User)
    for key, value in all_users.items():
        if user_id == value.id:
            keep_user = key
            break
    if keep_user:
        storage.delete(all_users[keep_user])
        storage.save()
        return Response(json.dumps({}, indent=2), mimetype="application/json",
                        status=200)
    abort(404)


@app_views.route("/users", methods=["POST"],
                 strict_slashes=False)
def post_user():
    """
        Creates a User object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    if not data.get("email"):
        return "Missing email", 400
    if not data.get("password"):
        return "Missing password", 400
    instance = User()
    for key, val in data.items():
        setattr(instance, key, val)
    instance.save()
    return Response(json.dumps(instance.to_dict(), indent=2),
                    mimetype="application/json", status=201)


@app_views.route("/users/<user_id>", methods=["PUT"],
                 strict_slashes=False)
def put_user(user_id):
    """
        Updates a User object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    all_users = storage.all(User)
    for user in all_users.values():
        if user_id == user.id:
            for key, val in data.items():
                if key == "id" or key == "email" or \
                   key == "created_at" or key == "updated_at":
                    continue
                setattr(user, key, val)
            storage.save()
            return Response(json.dumps(user.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)
