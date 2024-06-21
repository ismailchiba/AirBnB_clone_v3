#!/usr/bin/python3
"""
Perform REst API ACtions to state
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request
from flask import abort


@app_views.route('/states/',
                 strict_slashes=False, methods=['GET'])
def all_states():
    """listing all states in storage"""
    states = storage.all(State).values()
    return jsonify([state.to_dict() for state in states])


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['GET'])
def state_by_id(state_id):
    """retreiving state by id"""
    state = storage.all()
    for key, val in state.items():
        if val.to_dict().get('id') == state_id:
            return jsonify(val.to_dict())
    return (abort(404))


@app_views.route('/states/',
                 strict_slashes=False, methods=['POST'])
def post_state():
    """creating a new State"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    if 'name' not in data.keys():
        return (abort(400, 'Missing name'))
    state = State(**data)
    storage.new(state)
    storage.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    """update state by id"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    if 'name' not in data.keys():
        return (abort(400, 'Missing name'))
    state = storage.get(State, state_id)
    if not state:
        return (abort(404))
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for j, m in data.items():
        if j not in ignore_keys:
            setattr(state, j, m)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    """deleting a state by its id"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()
    return jsonify({}), 200
