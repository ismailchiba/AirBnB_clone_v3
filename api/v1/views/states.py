#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State


@app_views.route(
    '/states',
    methods=['GET'],
    strict_slashes=False
)
def get_all_states():
    """get all states"""
    states = storage.all(State)
    all_states = []
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route(
    '/states/<state_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_each_state(state_id):
    """get a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route(
    '/states',
    methods=['POST'],
    strict_slashes=False
)
def create_state():
    """create a state"""
    if not request.json:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.json:
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route(
    '/states/<state_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_state(state_id):
    """update a state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.json:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    for k, v in request.get_json().items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict())
