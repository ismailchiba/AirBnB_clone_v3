#!/usr/bin/python3
"""this file adds HTTP methods for the State model"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """gets a list of all states"""
    states_data = storage.all(State).values()
    states_list = []
    for state in states_data:
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state_id(state_id):
    """gets a specific state with state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state_id(state_id):
    """deletes a specific state with state_id"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state_id():
    """creates a specific state with state_id"""
    if request.headers['Content-Type'] != 'application/json':
        abort(415, description='Unsupported Media Type')

    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')
    if 'name' not in data:
        abort(400, description='Missing name')

    new_state = State(name=data['name'])
    storage.new(new_state)
    storage.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state_id(state_id):
    """updates a specific state with state_id"""
    state = storage.get(state.id)
    if not state:
        abort(404)

    data = request.get_json()
    if not data:
        abort(400, description='Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)


if __name__ == '__main__':
    app_views.run(debug=True)
