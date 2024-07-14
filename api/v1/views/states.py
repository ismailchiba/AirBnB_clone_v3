#!/usr/bin/python3
"""
Creates new view for State obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    states = storage.all(State).values()
    state_json = [state.to_dict() for state in states]
    return jsonify(state_json)


@app_views.route('states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_by_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    state = State(name=name)
    storage.new(state)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if name:
        setattr(state, 'name', name)
    storage.save()
    return jsonify(state.to_dict()), 200
