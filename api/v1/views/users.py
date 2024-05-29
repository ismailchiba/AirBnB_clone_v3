from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.user import User
from models import storage
import json

@app_views.route("/users/")
def get_users():
    """ return list of users"""

    users_dict = []
    for value in storage.all(User).values():
        users_dict.append(value.to_dict())
    return json.dumps(users_dict, indent=2) + '\n'


@app_views.route("/users/<user_id>")
def get_user(user_id):
    """ get specific user"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return json.dumps(user.to_dict(), indent=2) + '\n'


@app_views.route("/users/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    """ delete user provided ID"""

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return json.dumps({}, indent=2) + '\n'


@app_views.route("/users", methods=['POST'])
def create_user():
    """ create user object"""

    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, "NOT a JSON")
    if "password" not in obj_dict.keys():
        abort(400, "Missing password")
    if "email" not in obj_dict.keys():
        abort(400, "Missing email")


    obj = User(**obj_dict)
    storage.new(obj)
    storage.save()
    x = obj.to_dict()
    return json.dumps(x, indent=2) + '\n', 201

@app_views.route("/users/<user_id>", methods=["PUT"])
def user_update(user_id):
    """ update user """

    obj = storage.all(User)
    skip_keys = ["id", "created_at", "updated_at"]
    available = False
    for key in obj.keys():
        if key.split('.')[-1] == user_id:
            available = True
            user = obj[key]
            obj_dict = user.to_dict()
            break

    if available is False:
        abort(404)
    up_dict = request.get_json()
    if up_dict is None:
        abort(400, "Not a JSON")
    storage.delete(user)
    storage.save()
    for ky, value in up_dict.items():
        if ky not in skip_keys:
            obj_dict[ky] = value
    obj = User(**obj_dict)
    storage.new(obj)
    storage.save()
    return json.dumps(obj.to_dict(), indent=2) + '\n', 200 
