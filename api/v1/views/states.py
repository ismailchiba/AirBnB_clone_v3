#!/usr/bin/python3
"""A new view for State objects that handles
all default RESTFul API actions"""

from api.v1.views import app_views
from models import storage
from flask import abort, request, jsonify
from models.state import State


@app_views.route('/states/', methods=['GET', 'OPTIONS'])
def getStates():
    """A function to get states"""
    states = storage.all('State')
    all_states = []
    for state in states.values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', methods=['GET', 'OPTIONS'])
def getStateById(state_id):
    """A method to get state by id
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', methods=['DELETE', 'OPTIONS'])
def deleteStateById(state_id):
    """A method to delete state by id
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        storage.delete(state)
        storage.save()
        return {}, 200


@app_views.route('/states/', methods=['POST', 'OPTIONS'])
def createState():
    """A method to delete state by id
    """
    try:
        new_state = request.get_json()
        state_obj = State(**new_state)
        storage.new(state_obj)
        storage.save()
    except Exception as e:
        abort(400, 'Not a JSON')
    return jsonify(state_obj.to_dict())


@app_views.route('/states/<state_id>', methods=['PUT', 'OPTIONS'])
def editState(state_id):
    """A method to edit state by id
    """
    state = storage.get('State', state_id)
    print(state_id)
    print(state)
    if not state:
        print("Issue")
    else:
        try:
            request_json = request.get_json()
            for key, value in request_json.items():
                setattr(state, key, value)
        except Exception as e:
            abort(404, 'Not a valid JSON')
        state.save()
        return jsonify(state.to_dict()), 200
