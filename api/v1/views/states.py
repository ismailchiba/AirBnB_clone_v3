#!/usr/bin/python3
"""Import required module/lib"""
from flask import jsonify, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'])
def get_states():
    """Retrieve all states"""
    states = storage.all(State)
    return jsonify([state.to_json() for state in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieve a state by id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Delete a state by id"""
    if state is None:
        abort(404)
    storage.delete(state_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """
    Create a new state
    """
    if not request.json:
        abort(400, "Not a JSON")
    if 'name' not in request.json:
        abort(400, "Missing name")
    data = request.json
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """
    Update a state by id
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, "Not a JSON")
    data = request.json
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
