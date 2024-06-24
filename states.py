#!/usr/bin/python3
''' new view for State objects'''
from flask import Flask, jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    '''Gets all State objects'''
    states = storage.all(State)
    return jsonify([state.to_dict() for state in states.values()])

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    '''Gets a specific State object by id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates a new State object'''
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    state = State(**request.json)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates a State object by id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    '''Deletes a State object by id'''
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200