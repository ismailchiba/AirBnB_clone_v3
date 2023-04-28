#!/usr/bin/python3
"""A view for State objects that handles all default
RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State


@app_views.route('/states')
def get_all_states():
    """Returns all json representation of States"""
    states = storage.all(State)
    return jsonify([x.to_dict() for x in states.values()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
    """Returns a json representation of a matching state"""
    state = storage.all(State).get(State.__name__ + '.' + state_id, None)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a State object from storage"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """Create a new State object from POST json data"""
    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400
    elif 'name' not in data:
        return 'Missing name', 400
    state = State(name=data['name'])
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Update State object data from PUT json data"""

    state = storage.all(State).get(State.__name__ + '.' + state_id, None)
    if state is None:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        return 'Not a JSON', 400
    if type(data) is not dict:
        return 'Forbidden', 400

    for key in ['created_at', 'updated_at']:
        try:
            data.pop(key)
        except KeyError:
            pass

    for key, value in data.items():
        setattr(state, key, value)

    state.save()
    return jsonify(state.to_dict()), 200
