#!/usr/bin/python3
"""Module for the view of State objects
that handles all default RESTFul API actions """

from api.v1.views import app_views
from models.state import State
from models import storage
from flask import jsonify, abort, request


# Using to_dict() to retrieve an object into a valid JSON
# Retrieves the list of all State objects: GET /api/v1/states
@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_states():
    """Retrieves the list of all State objects"""
    states =[state.to_dict() for state in storage.all(State).values()]
    return jsonify(states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """Retrieves the state by its id"""
    states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in states if obj.id == state_id]
    if not state_obj:
        abort(404)
    return jsonify(state_obj)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """Deletes a state by id"""
    states = storage.all(State).values()
    state_obj = [obj.to_dict() for obj in states if obj.id == state_id]
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
