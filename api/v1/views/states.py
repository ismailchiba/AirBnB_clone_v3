#!/usr/bin/python3
"""
the blueprint the handle app view and state view
"""


from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import abort
from flask import request
from models.state import State


@app_views.route("/states", methods=['GET'], strict_slashes=False)
def get_states():
    """get states"""
    states = [state for state in storage.all(State).values()]
    return jsonify([state.to_dict() for state in states])


@app_views.route("/states/<state_id>", methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get states"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route("/states/<state_id>", methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """get states"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()

        return jsonify({}), 200
    else:
        abort(404)


@app_views.route("/states/", methods=['POST'], strict_slashes=False)
def create_state():
    """create states"""
    dic_t = request.get_json()
    if not dic_t:
        abort(400, "Not a JSON")
    if "name" not in dic_t:
        abort(400, "Missing name")
    state = State(**dic_t)
    state.save()
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update states"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    dic_t = request.get_json()
    if not dic_t:
        abort(400, "Not a JSON")
    for key, value in dic_t.items():
        setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
