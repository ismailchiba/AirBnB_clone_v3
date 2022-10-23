#!/usr/bin/python3
""" A new view for State objects that handles
all default RESTFul API actions. """
from api.v1.views import app_views
from flask import request, jsonify, abort, make_response
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET", "POST"])
def get_states():
    """ Retrieves the list of all State objects."""

    if request.method == "GET":
        all_states = storage.all(State)
        list_states = []
        for state in all_states:
            list_states.append(state.to_dict())
        return jsonify(list_states)

    if request.method == "POST":
        if request.is_json is False:
            abort(400, "Not a JSON")
        state_req = request.get_json()
        if "name" not in state_req:
            abort(400, "Missing name")
        new_state = State(**state_req)
        new_state.save()
        return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route("/states/<state_id>", methods=["GET", "DELETE", "PUT"])
def handle_state(state_id=None):
    """Get, Delete or Update a state by id"""

    state = storage.get(State, state_id)

    if state is None:
        abort(404)

    if request.method == "GET":
        return jsonify(state.to_dict())

    if request.method == "DELETE":
        state.delete()
        storage.save()
        return make_response(jsonify({}), 200)

    if request.method == "PUT":
        if request.is_json is False:
            abort(400, "Not a JSON")
        state_req = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']
        for key, val in state_req.items():
            if key not in ignore_keys:
                setattr(state, key, val)
        storage.save()
        return make_response(jsonify(state.to_dict()), 200)
