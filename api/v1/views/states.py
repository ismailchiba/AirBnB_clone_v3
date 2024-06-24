#!/usr/bin/python3
""" View for State object """

from flask import jsonify, request, abort, make_response
from models import storage
from datetime import datetime
from models.state import State
import uuid
from api.v1.views import app_views


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """ Retrieves list of all states """
    states = storage.all(State).values()
    list_states = []
    for state in states:
        list_states.append(state.to_dict())
    return (jsonify(list_states))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves States object define by id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return (jsonify(state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """ Deletes a state """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """ Create new state """
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'name' not in response:
        abort(400, 'Missing name')
    new_state = State(**response)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/state/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Update a state """
    state = Storage.get(State, state_id)
    if state is None:
        abort(404)
    keys = ['id', 'created_at', 'updated_at']
    response = request.get_json()
    if 'name' not in response:
        abort(400, 'Not a JSON')
    for key, value in response.items():
        if key not in keys:
            setattr(state, key, value)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
