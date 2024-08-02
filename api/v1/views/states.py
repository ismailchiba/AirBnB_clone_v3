#!/usr/bin/python3
""" API endpoints for states """

from models import storage
from models.state import State

from flask import jsonify, abort, request

from api.v1.views import app_views

STATES_SEGMENT = 'states'


@app_views.route(f'/{ STATES_SEGMENT }', methods=['GET'], strict_slashes=False)
def get_states():
    """ Gets all states """
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route(f'/{ STATES_SEGMENT }/<state_id>',
                 methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Gets a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(f'/{ STATES_SEGMENT }/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route(f'/{ STATES_SEGMENT }',
                 methods=['POST'], strict_slashes=False)
def create_state():
    """ Creates a state """
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route(f'/{ STATES_SEGMENT }/<state_id>',
                 methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a state by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    forbidden_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
