#!/usr/bin/python3
"""Module that handles all default RESTful API actions for States class"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def retrieve_states():
    """retrieves a all State objects"""

    states = storage.all(State).values()

    state_list = [state.to_dict() for state in states]

    return jsonify(state_list)


@app_views.route("/states/<id>", methods=["GET"], strict_slashes=False)
def retrieve_state(id):
    """retrieves a State object based on its id"""

    state = storage.get(State, id)

    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """creates a state object"""

    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    if body.get("name") is None:
        abort(400, "Missing name")

    new_state = State(**body)
    storage.new(new_state)
    storage.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<id>", methods=["PUT"], strict_slashes=False)
def update_state(id):
    """updates a state object by id"""

    state = storage.get(State, id)

    if state is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    excluded_keys = ["id", "created_at", "updated_at"]

    for key, value in body.items():
        if key not in excluded_keys:
            setattr(state, key, value)

    storage.save()

    return jsonify(state.to_dict()), 200


@app_views.route("/states/<id>", methods=["DELETE"], strict_slashes=False)
def delete_state(id):
    """deletes a state object by id"""
    state = storage.get(State, id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
