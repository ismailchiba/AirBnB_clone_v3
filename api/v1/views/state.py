#!/usr/bin/python3
"""
    A module for states
"""
from api.v1.views import (app_views, State, storage)
from flask import (abort, jsonify, make_response, request)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def view_all_states():
    """
    Retrieves a list of all the states
    """
    state_list = [state.to_json() for state in storage.all("State").values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def view_one_state(state_id=None):
    """i
    Retrieves a state by a given id
    """
    if state_id is None:
        abort(404)
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    storage.delete(state_obj)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State object based on the JSON body
    """
    res = None
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if 'name' not in res.keys():
        return "Missing name", 400
    new_state = State(**res)
    new_sate.save()
    return jsonify(new_state.to_json()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """
    Updates a State object based on the JSON body
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    state_obj = storage.get("State", state_id)
    if state_obj is None:
        abort(404)
    for item in ("id", "created_at", "updated_at"):
        res.pop(item, None)
    for key, value in res.items():
        setattr(state, key, value)
    state.save()
    return jsonify(state.to_json()), 200
