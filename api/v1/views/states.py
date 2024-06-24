#!/usr/bin/python3
"""Create a new view for State objects that handles all default RESTFul API actions:"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all():
    states_dict = []
    for state in storage.all(State).values():
        states_dict.append(state.to_dict())
    return jsonify(states_dict)

@app_views.route('/states/<path:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())

@app_views.route('/states/<path:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    state = request.get_json()
    if type(state) != dict:
        return abort(400, {'message': 'Not a JSON'})
    if 'name' not in state: 
        return abort(400, {'message': 'Missing name'})
    buff = State(**state)
    buff.save()
    return jsonify(buff.to_dict()), 201

@app_views.route('/states/<path:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_req = request.get_json()
    if type(state_req) != dict:
        return abort(400, {'message': 'Not a JSON'})
    for x, y in state_req.items():
        if x not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(state, x, y)
    storage.save()
    return jsonify(state.to_dict()), 200

