#!/usr/bin/python3
"""states"""


from api.v1.views import app_views
from flask import Flask, jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get all states"""
    x = [i.to_dict() for i in storage.all(State).values()]
    return jsonify(x)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get a state"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({})
    abort(404)

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict()), 200
