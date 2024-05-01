#!/usr/bin/python3
"""REST API routes for State objects"""

from api.v1.views import app_views, jsonify
from models.state import State
from models import storage
from flask import abort, make_response, request


# GET Requests


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    list_states = []
    objs = storage.all(State)
    for obj in objs.values():
        list_states.append(obj.to_dict())

    return jsonify(list_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State object by its ID"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    else:
        return jsonify(state_obj.to_dict())


# DELETE Request


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_state(state_id):
    """Delete a state object from the storage by its ID"""
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)

    storage.delete(state_obj)
    storage.save()
    return make_response(jsonify({}), 200)


# POST Request


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    """Create a new State object"""

    if not request.get_json():
        abort(400, description="Not a JSON")
    if "name" not in request.get_json():
        abort(400, description="Missing name")

    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


# PUT Request


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates an existing State object"""
    state_obj = storage.get(State, state_id)

    if state_obj is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")

    request_dict = request.get_json()
    ignored_attrs = ["id", "created_at", "updated_at"]
    for key, value in request_dict.items():
        if key not in ignored_attrs:
            setattr(state_obj, key, value)

    storage.save()
    return make_response(jsonify(state_obj.to_dict()), 200)
