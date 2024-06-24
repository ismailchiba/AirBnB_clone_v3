#!/usr/bin/python3
"""this module handles all default RESTFul API actions"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views

import models
from models.state import State


@app_views.route('/states', strict_slashes=False, methods=['GET'])
def get_states():
    all_states = models.storage.all(State)
    states = [x.to_dict() for x in all_states.values()]
    return jsonify(states)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """ Retrieves a specific State """
    state = models.storage.get(State, state_id)
    if not state:
        abort(404)

    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State Object
    """

    state = models.storage.get(State, state_id)

    if not state:
        abort(404)

    models.storage.delete(state)
    models.storage.save()

    return jsonify({}), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """
    Creates a State
    """
    if not request.get_json():
        abort(400, description="Not a JSON")

    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data = request.get_json()
    instance = State(**data)
    models.storage.new(instance)
    models.storage.save()
    return jsonify(instance.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    """
    Updates a State
    """
    state = models.storage.get(State, state_id)

    if not state:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    ignore = ['id', 'created_at', 'updated_at']

    data = request.get_json()
    for key, value in data.items():
        if key not in ignore:
            setattr(state, key, value)
    models.storage.save()
    return jsonify(state.to_dict()), 200
