#!/usr/bin/python3
"""State view"""
from api.v1.views import state_views
from models import storage
from flask import abort, request, jsonify


@state_views.route('/states', methods=["GET"], strict_slashes=False)
def get_states():
    """Return all states"""
    return [state.to_dict() for state in storage.all("State").values()]


@state_views.route('/states/<states_id>', methods=["GET"], strict_slashes=False)
def get_states_id(states_id):
    """Return states specific to an id else return 404"""
    result = [state.to_dict() for state in storage.all(
        "State").values() if state.id == states_id]
    if result == []:
        abort(404)
    return result


@state_views.route('/states/<states_id>', methods=["Delete"], strict_slashes=False)
def delete_states_id(states_id):
    """Delete states specific to an id else return 404"""
    state = storage.get("State", states_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@state_views.route('/states', methods=["POST"], strict_slashes=False)
def post_states():
    """Post states"""
    from models.state import State
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    if "name" not in request.json:
        return jsonify({"error": "Missing name"}), 400
    state = State(**request.json)
    state.save()
    return state.to_dict(), 201


@state_views.route('/states/<states_id>', methods=["PUT"], strict_slashes=False)
def put_state(states_id):
    """Put states"""
    state = storage.get("State", states_id)
    if state is None:
        abort(404)
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in request.json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
    state.save()
    return state.to_dict(), 200
