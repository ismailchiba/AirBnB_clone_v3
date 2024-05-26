#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    return jsonify(State.all())


def handle_E(error, message="Not found", code=404):
    """Custom handler for 404 errors."""
    response = jsonify({"error": message})
    response.status_code = code
    return response


@app_views.route('/states/<state_id>', strict_slashes=False)
@app_views.route('/states', strict_slashes=False)
def get_states(state_id=None):
    """
    returns a state if state_id provided, otherwise all states"""
    try:
        tmp = State.to_dict(storage.get(State, state_id)) if state_id else\
                [State.to_dict(obj) for obj in storage.all(State).values()]
        return jsonify(tmp)
    except KeyError:
        return handle_E()


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_state(state_id=None):
    """delete state object"""
    st = storage.get(State, state_id)
    if st:
        tmp = State.delete(st)
        return jsonify({})
    else:
        return handle_E()


@app_views.route('/states', strict_slashes=Falsei, methods=['POST'])
def add_state(state_id=None):
    """add new state object"""
    data = request.get_json(silent=True)
    if data is None:
        return handle_E(message="Not a JSON", code=400)
    if data.get(name) is None:
        return handle_E(message="Missing name", code=400)
    st = State(data.get(name))
    storage.new(st)
    tmp = State.to_dict(st)
    tmp.status_code = 201
    return jsonify(tmp)


@app_views.route('/states/<state_id>', strict_slashes=Falsei, methods=['PUT'])i
def update_state(state_id=None):
    """add new state object"""
    st = storage.get(State, state_id)
    if st is None:
        return handle_E()

    data = request.get_json(silent=True)
    if data is None:
        return handle_E(message="Not a JSON", code=400)
    if data.get(name) is None:
        return handle_E(message="Missing name", code=400)
    st = State(data.get(name))
    storage.new(st)
    tmp = State.to_dict(st)
    tmp.status_code = 201
    return jsonify(tmp)
