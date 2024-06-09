#!/usr/bin/python3
""" objects that handles all default RestFul API actions for States"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_state():
    """Retrieves the list of all State objects"""
    all_states = storage.all(State).values()
    list_state = []
    for state in all_states:
        list_state.append(state.to_dict())
    return jsonify(list_state)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_id(state_id):
    """Retrieves a State by id"""
    state = storage.get(State, state_id)

    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def delete_state_id(state_id):
    """Deletes a State object by id"""
    state = storage.get(State.state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not "name" in request.json():
        abort(400, "Missing name")

    state = request.json()
    instance = State(**state)
    storage.new(instance)
    storage.save()

    return make_response(jsonify(state), 201)


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """Updates a State object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not "name" in request.get_json():
        abort(400, "Missing name")

    if not storage.get(State, state_id):
        abort(404)

    state = storage.get(State, state_id)
    state_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()

    return make_response(jsonify(state), 200)
