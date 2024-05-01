#!/usr/bin/python3
"""
create states
"""
from flask import jsonify
from flask import abort
from flask import request
from models.state import State
from models import storage
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'],
                 strict_slashes=False)
def get_all_states():
    """
    Get all states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/state/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state_by_id(state_id):
    """
    Get state by id
    """
    try:
        state = storage.get(State, state_id)
        return jsonify(state.to_dict())
    except Exception:
        abort(404)


@app_views.route('/state/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state_by_id(state_id):
    """
    Delete state by id
    """
    try:
        state = storage.get(State, state_id)
        storage.delete(state)
        return jsonify({}), 200
    except Exception:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    states = []
    new_state = State(name=request.json['name'])
    storage.new(new_state)
    storage.save()
    states.append(new_state.to_dict())
    return jsonify(states[0]), 201


@app_views.route('/state/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state_id(state_id):
    """
    Update state
    """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in data.items():
            if key not in ignore_keys:
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict()), 200
    else:
        return abort(404)
