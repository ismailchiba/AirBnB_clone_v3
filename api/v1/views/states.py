#!/usr/bin/python3
""" this module contain state views GET, PUT,
    DELETE, POST http methods for state objects"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.base_model import BaseModel
from models.state import State
from models import storage


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """ return states """

    states_list = []
    for value in storage.all(State).values():
        states_list.append(value.to_dict())
    return jsonify(states_list)


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ get state from provided ID"""

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ delete state provided ID"""

    states = storage.all(State)
    if len(states) == 0:
        abort(404)
    for state in states.values():
        if state.id == state_id:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """ create state object"""

    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, description="NOT a JSON")
    if "name" not in obj_dict:
        abort(400, description="Missing name")

    state = State(**obj_dict)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """ update state """

    skip_keys = ["id", "created_at", "updated_at"]

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    update_dict = request.get_json()
    if update_dict is None:
        abort(400, description="Not a JSON")

    for key, value in update_dict.items():
        if key not in skip_keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
