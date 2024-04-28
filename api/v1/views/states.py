#!/usr/bin/python3
"""Handles State objects for RESTful API actions
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
def all_states():
    """gets and creates objects of State object"""
    if request.method == 'GET':
        all_states = storage.all(State)
        states = [obj.to_dict() for obj in all_states.values()]
        return jsonify(states)

    if request.method == 'POST':
        if not request.get_json():
            abort(400, 'Not a JSON')
        if 'name' not in request.get_json():
            abort(400, 'Missing name')
        new_state = State(name=request.json['name'])
        storage.new(new_state)
        storage.save()
        return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def states_by_id(state_id):
    """gets, deletes, and updates objects of State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())

    if request.method == 'DELETE':
        storage.delete(state)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json
        for key in req_json.keys():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, req_json[key])
        storage.save()
        return jsonify(state.to_dict()), 200
