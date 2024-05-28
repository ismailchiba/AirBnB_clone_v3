#!/usr/bin/python3
"""
Script that create a new view for State object that handles all defaualt
RESTful API.
"""
from flask import Flask, jsonfy, request, abort
from api.v1.views import app_views
from models import storage, state


@app_views.route('/states', methods=['Get'])
def get_states():
    state = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states', methods=['POST'])
def create_state():
    data = request.get_joson()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states', methods=['PUT'])
def state_update(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    datat = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', "created_at", "update_ at"]:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

