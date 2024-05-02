#!/usr/bin/python3
"""
State objects that handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/states', strict_slashes=False)
def get_states():
    """Get states instances"""
    states = storage.all(State).values()
    lst_state = [state.to_dict() for state in states]
    return jsonify(lst_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """getting state depending on the given id"""
    state = storage.get(State, state_id)

    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """deleting a state depending on the given id"""
    state = storage.get(State, state_id)

    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """creating a state """
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    element = request.get_json()

    if 'name' not in element:
        return abort(400, "Missing name")

    state = State(**element)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """updating client state """
    if request.content_type != 'application/json':
        return abort(400, "Not a JSON")
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, "Not a JSON")
        get_data = request.get_json()
        not_key = ['id', 'created_at', 'updated_at']

        for k, v in get_data.items():
            if k not in not_key:
                setattr(state, k, v)
            state.save()
            return jsonify(state.to_dict()), 200
        else:
            return abort(404)
