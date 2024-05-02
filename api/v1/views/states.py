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
    all_state = [i.to_dict() for i in storage.all(State).values()]
    return jsonify(all_state)


@app_views.route(
    '/states/<state_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_each_state(state_id):
    """get a state"""
    i = storage.get(State, state_id)
    if i is None:
        abort(404)
    return jsonify(i.to_dict())


@app_views.route(
    '/states/<state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
    """delete a state"""
    i = storage.get(State, state_id)
    if i is None:
        abort(404)
    storage.delete(i)
    storage.save()
    return jsonify({})


@app_views.route(
    '/states',
    methods=['POST'],
    strict_slashes=False
)
def create_state():
    """create a state"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if "name" not in data:
        abort(400, 'Missing name')
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route(
    '/states/<state_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_state(state_id):
    """update a state"""
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state, k, v)
    storage.save()
    return jsonify(state.to_dict())
