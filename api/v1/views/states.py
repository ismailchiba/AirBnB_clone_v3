#!/usr/bin/python3
"""Handles all default RESTFul API actions:"""

from flask import jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def state_list():
    """Retrieves the list of all State objects"""
    state_list = storage.all(State).values()
    list_of_states = []
    for state in state_list:
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)


@app_views.route('/status/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """Retrieves a State objects"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        return abort(404)
    else:
        return jsonify(state_obj)


@app_views.route('/status/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """Deletes a State object"""
    state_obj = storage.get(State, state_id)
    if not state_obj:
        return abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
        return jsonify({"status": 200})
