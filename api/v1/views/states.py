#!/usr/bin/python3
"""
Route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieves all State objects
    :return: JSON of all states
    """
    states = storage.all("State").values()
    return jsonify([state.to_json() for state in states])


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Create state route
    :return: Newly created state object
    """
    state_json = request.get_json(silent=True)
    if not state_json:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()

    return jsonify(new_state.to_json()), 201


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Gets a specific State object by ID
    :param state_id: state object ID
    :return: State object with the specified ID or error
    """
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    return jsonify(state.to_json())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Updates specific State object by ID
    :param state_id: state object ID
    :return: State object and 200 on success, or 400 or 404 on failure
    """
    state_json = request.get_json(silent=True)
    if not state_json:
        abort(400, 'Not a JSON')
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, val)
    state.save()
    return jsonify(state.to_json())


@app_views.route(
    "/states/<state_id>",
    methods=["DELETE"],
    strict_slashes=False
)
def state_delete_by_id(state_id):
    """
    Deletes State by ID
    :param state_id: state object ID
    :return: Empty dict with 200 or 404 if not found
    """
    state = storage.get("State", state_id)

    if not state:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({})
