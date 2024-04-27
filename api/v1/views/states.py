#!/usr/bin/python3

from flask import jsonify
from models import storage
from api.v1.views import app_views


@app_views.route('/states', strict_slashes=False)
def all_states():
    """
    Retrieves  the list of all State objects
    """
    print(storage.all("State"))
    states_obj = []

    for value in storage.all("State").values():
        states_obj.append(value)


    print(states_obj)


    # return jsonify(storage.all("State"))
