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


@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """get a state"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<string:state_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_state(state_id):
    """delete a state"""
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """create a state"""
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    if 'name' not in data:
        return make_response(
            jsonify({"error": "Missing name"}), 400
        )
    new_state = State(**data)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """update a state"""
    data = request.get_json()
    if data is None:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    state = storage.get(State, str(state_id))
    if state is None:
        abort(404)
    ignore_keys = ['id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    state.save()
    return jsonify(state.to_dict()), 200
