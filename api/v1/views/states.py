#!/usr/bin/python3
"""Handles all default RESTFul API actions:"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def state_list():
    '''Retrieves the list of all State objects'''
    state_list = storage.all(State).values()
    list_of_states = []
    for state in state_list:
        list_of_states.append(state.to_dict())
    return jsonify(list_of_states)
