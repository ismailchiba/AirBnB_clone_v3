#!/usr/bin/python3

from flask import abort, jsonify

from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_state():
    """Return all states"""
    states_list = []
    states_obj = storage.all(State)

    for obj in states_obj.values():
        states_list.append(obj.to_dict())

    response = jsonify(states_list), 200

    return response
