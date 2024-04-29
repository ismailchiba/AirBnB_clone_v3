#!/usr/bin/python3
"""Create Routing for  states using app_views template,
 create update get and delete
 """
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import request, jsonify


@app_views.route('/states', methods=('GET', 'POST'), strict_slashes=False)
def states():
    """Handle GET and POST methods"""
    if request.method == 'GET':
        states = [state.to_dict() for state in storage.all(State).values()]
        return jsonify(states)
    elif request.method == 'POST':
        req = request.get_json()
        if req is None:
            return (jsonify({'error': 'Not a JSON'}), 400)
        if req['name'] is None:
            return (jsonify({'error': 'Missing name'}), 400)
        newState = State(**req)
        storage.new(newState)
        storage.save()
        return jsonify(newState.to_dict()), 201


@app_views.route('/states/<state_id>',
                 methods=('GET', 'PUT', 'DELETE'), strict_slashes=False)
def stateId(state_id=None):
    """display the states and cities listed in alphabetical order"""
    if state_id is not None:
        state = storage.get(State, state_id)
        if request.method == 'GET':
            if state is not None:
                return jsonify(state.to_dict())
            else:
                return (jsonify({'error': 'Not found'}), 404)
        if request.method == 'PUT':
            if state is not None:
                req = request.get_json()
                if req is None:
                    return (jsonify({'error': 'Not a JSON'}), 400)
                for key, val in req.items():
                    if key not in ["id", "created_at", "updated_at"]:
                        setattr(state, key, val)
                state.save()
                return jsonify(state.to_dict()), 200
            else:
                return (jsonify({'error': 'Not found'}), 404)
        if request.method == 'DELETE':
            if state is not None:
                storage.delete(state)
                storage.save()
                return jsonify({}), 200
