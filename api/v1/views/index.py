#!/usr/bin/python3
#"""defines api status"""
from api.v1.views import app_views
from flask import Flask, jsonify, request, abort
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    #"""return status"""
    key = "status"
    return jsonify({"status": "OK"})

@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    #"""Return the number of each objects by type."""
    counts = storage.count()
    print(f"couunts from storage.count: {counts}")
    return jsonify(counts)

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    #""""retrieve the list of all state objects"""
    all_states = storage.all(State) # dictionary of all states
    states_list = [state.to_dict() for state in all_states.values()]
    return jsonify(states_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    # retrieve a state object
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    # create a new state object
    if not request.json or 'name' not in request.json:
        abort(400, 'Not a JSON')
    if not request.json['name'] or not isinstance(request.json['name'], str):
        abort(400, 'Missing name')
    state = State(**request.get_json())
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201

@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    # update a state object
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.json.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict())

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    # delete a state object
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description='Not found')
    try:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200 | '', 204
    except Exception as e:
        abort(500, description=str(e))
