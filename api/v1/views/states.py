#!/usr/bin/python3
"""A new view for State objects
that handles all default RESTFul API actions"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def states_obj():
    """Retrieve an object into a valid JSON"""
    obj_state = storage.all(State).values()
    if obj_state is None:
        abort(404)

    state_all = []
    for obj_s in obj_state:
        dict_state = obj_s.to_dict()
        state_all.append(dict_state)
    return jsonify(state_all)


@app_views.route("/states/<state_id>",
                 methods=["GET"], strict_slashes=False)
def states_obj_id(state_id):
    """Retrieve an object into a valid JSON by an ID"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    return jsonify(obj_state.to_dict())


@app_views.route("/states/<state_id>",
                 methods=["DELETE"], strict_slashes=False)
def states_delete(state_id):
    """Delete an object by an ID"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)
    storage.delete(obj_state)
    storage.save()
    return jsonify({}), 200


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def states_post():
    """Create a new obj"""
    data = request.get_json()

    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    new_state = State(**data)
    new_state.save()

    return jsonify(new_state.to_dict()), 201


@app_views.route("/states/<state_id>",
                 methods=["PUT"], strict_slashes=False)
def states_put(state_id):
    """Update obj by an ID"""
    obj_state = storage.get(State, state_id)
    if obj_state is None:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in data:
        return jsonify({"error": "Missing name"}), 400

    for key, value in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(obj_state, key, value)
    storage.save()
    return jsonify(obj_state.to_dict()), 200
