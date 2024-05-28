#!/usr/bin/python3
"""State module"""
from flask import Flask, jsonify, abort, request
from models import storage
from models.state import State
from api.v1.views import app_views
from flasgger.utils import swag_from


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get.yml', methods=['GET'])
def get_states():
    """Retrieve all state"""
    all_states = storage.all(State).values()
    state_list = [state.to_dict() for state in all_states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
@swag_from('documentation/state/get_id.yml', methods=['GET'])
def get_state(state_id):
    """ retrieves a state object """
    state = storage.get(State, statee_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
@swag_from('documentation/state/delete.yml', methods=['DELETE'])
def delete_state(state_id):
    """ Deletes a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
@swag_from('documentation/state/post.yml', methods=['POST'])
def create_state():
    """Creates a State"""
    if not request.is_json:
        abort(400, description="Not a JSON")
    state_data = request.get_json()
    if 'name' not in state_data:
        abort(400, description="Missing name")
    new_state = State(**state_data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
@swag_from('documentation/state/put.yml', methods=['PUT'])
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.is_json:
        abort(400, description="Not a JSON")
    state_data = request.get_json()
    ignore_keys = ['id', 'created_at', 'updated_at']
    for key, value in state_data.items():
        if key not in ignore_keys:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200
