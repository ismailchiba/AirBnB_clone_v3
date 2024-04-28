#!/usr/bin/python3
"""Handles State objects for RESTful API actions
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, abort, jsonify, make_response


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def all_get_states():
    """gets objects of State object"""
    all_states = storage.all(State)
    states = [obj.to_dict() for obj in all_states.values()]
    return jsonify(states)


@app_views.route('/states/', methods=['POST'],
                 strict_slashes=False)
def post_state():
    """creates objects of State object"""
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}))
    if 'name' not in request.get_json():
        return make_response(jsonify({'error': 'Missing name'}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_states_by_id(state_id):
    """gets objects of State object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """deletes a State object by ID"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """updates a State object by ID"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
