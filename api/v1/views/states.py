#!/usr/bin/python3
"""view for State objects that handles all default RESTFul API actions"""

from . import app_views
from flask import jsonify
from models.state import State
from models import storage


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def all_state():
    """retrieves the list of all state objects"""
    allState = storage.all(State)
    statelist = []

    for states in allState.items():
        stateDict.append(states.to_dict())

    return jsonify(stateDict)
