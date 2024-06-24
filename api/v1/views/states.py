#!/usr/bin/python3
"""
new view for state
"""
from flask import jsonify, request, abort
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieve list of all State objects."""
    state_list = []
    state_obj = storage.all("State")
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)

@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """ Creates a new state and returns newly created state object."""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp

