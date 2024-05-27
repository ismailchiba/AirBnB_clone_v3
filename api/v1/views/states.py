#!/usr/bin/python3
"""states api view module"""
from api.v1.views import app_views
from flask import (
    abort,
    jsonify,
    make_response,
    request
)
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_states():
    """Retrieves the list of all State objects: GET /api/v1/states"""
    all_states = storage.all(State).values()
    state_list = [all_states.to_dict() for state in all_states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id=None):
    """Retrieves a State object: GET /api/v1/states/<state_id>"""
    if state_id is None:
        return abort(404)
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        return abort(404)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    """Deletes a State object:: DELETE /api/v1/states/<state_id>"""
    if state_id is None:
        abort(404)
    state = storage.get(State, state_id)
    if state:
        storage.delete(State, state_id)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Creates a State: POST /api/v1/states"""
    if request.content_type != 'application/json':
        return abort(404, 'Not a JSON')
    if not request.get_json():
        return abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'name' not in kwargs:
        abort(400, 'Missing name')

    state = State(**kwargs)
    state.save()
    return jsonify(state.to_dict()), 200


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    """Updates a State object: PUT /api/v1/states/<state_id>"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if state:
        if not request.get_json():
            return abort(400, 'Not a JSON')
        obj = request.get_json()
        ignore_keys = ['id', 'created_at', 'updated_at']

        for key, value in obj.items():
            if key not in ignore_keys:
                setattr(sate, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
    else:
        return abort(404)
