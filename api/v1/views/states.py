#!/usr/bin/python3
"""Module for the view of State objects
that handles all default RESTFul API actions """


from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """Retrieves the state by its id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    return jsonify(state_obj)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a state by id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    storage.delete(state_obj)
    atorage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a new state"""
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    new_state = State(**data)
    storage.new(new_state)
    storage.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates the state based on the id"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(state_obj, k, v)
        storage.save()
        return jsonify(state_obj.to_dict()), 200
