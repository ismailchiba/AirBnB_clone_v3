#!/usr/bin/python3
"""State objects that handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from models import storage
from models.state import State
from api.v1.views import app_views


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def all_states():
    return jsonify([state.to_dict() for state in storage.all(State).values()])


@app_views.route("/states/<state_id>", methods=["GET"])
def get_state(state_id):
    state = storage.get(State, state_id)
    return jsonify(state.to_dict()) if state else abort(404)


@app_views.route("/states/<state_id>", methods=["DELETE"])
def del_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def post_state():
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=["PUT"])
def put_state(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ("id", "created_at", "updated_at"):
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
