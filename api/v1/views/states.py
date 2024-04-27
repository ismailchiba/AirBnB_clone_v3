#!/usr/bin/python3
"""states.py"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State

# Endpoint to retrieve all State objects
@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    """get state information for all states"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])

# Endpoint to retrieve a specific State object by state_id
@app_views.route('/states/<state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """ get state information based on id"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a state based on its state_id"""
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def post_state():
    """create a new state"""
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'name' not in data:
        abort(400, "Missing name")
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'],
                 strict_slashes=False)
def put_state(state_id):
    """update a state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    storage.save()
    return jsonify(state.to_dict()), 200