#!/usr/bin/python3
"""states.py"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """Retrieves all State objects"""
    states = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        states.append(obj.to_json())

    return jsonify(states)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """Create a new State object"""
    data = request.get_json(silent=True)
    if not data:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')

    new_state = State(**data)
    new_state.save()
    response = jsonify(new_state.to_json())
    response.status_code = 201

    return response


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """Retrieve a specific State object by ID"""
    state = storage.get("State", str(state_id))

    if state is None:
        abort(404)

    return jsonify(state.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """Updates specific State object by ID"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)
    for key, val in data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """Deletes a specific State object by ID"""
    state = storage.get("State", str(state_id))
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({})
