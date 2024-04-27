#!/usr/bin/python3
"""
This file defines the routes to perform operations
on the States class
"""

from flask import jsonify, abort
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def get_all_states():
    """
    Retrieves  the list of all State objects
    """
    states_obj = []

    for value in storage.all("State").values():
        states_obj.append(value.to_dict())

    return jsonify(states_obj)


@app_views.route("/states/<state_id>", strict_slashes=False)
def one_state(state_id):
    """
    this method returns a specific state depending on the
    id passed in
    """
    all_states = storage.all("State")

    for value in all_states.values():
        if value.id == state_id:
            return jsonify(value.to_dict())

    abort(404)
