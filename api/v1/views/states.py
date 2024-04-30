#!/usr/bin/python3
"""Handles all default RESTFul API actions:"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def state_list():
    """Retrieves the list of all State objects"""
    state_list = storage.all(State).values()
    list_of_states = []
    for state in state_list:
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)


@app_views.route('/status/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State objects"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        return abort(404)
    else:
        return jsonify(state_obj)


@app_views.route('/status/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        return abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
        return jsonify({"status": 200})


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State"""
    post_data = request.get_json()
    if not post_data:
        abort(400, description="Not a JSON")

    if 'name' not in post_data:
        abort(400, description="Missing name")

    new_state = State(**post_data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strictslashes=False)
def update_state_by_id(state_id):
    """Updates state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
            storage.save()
    return jsonify(state.to_dict()), 200
