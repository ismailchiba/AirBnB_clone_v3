#!/usr/bin/python3
"""
retrieves list of all state objects, the state object, deletes creates and updates a state object
"""
from flask import jsonify
from models.state import State
from models import storage
from api.v1.views import app_views
from flask import request, abort


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """
    Retrieves the list of all State objects: GET /api/v1/states
    """
    states = storage.all(State).values()
    state_list = [state.to_dict()for state in states]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_state(state_id):
    """
    Retrieves a State object: GET /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    """
    state = storage.get('State', state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    """
    Deletes a State object: DELETE /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    state = storage.get('State', state_id)
    if state:
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """
    Creates a State: POST /api/v1/states
    You must use request.get_json from Flask to transform the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
    Returns the new State with the status code 201  
    """
    if request.is_json:
        kwargs = request.get_json()

        if 'name' not in kwargs:
            abort(400, 'Missing Name')

        state = State(**kwargs)
        state.save()
        return jsonify(state.to_dict()), 201
    abort(400, 'Not a JSON')


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """
    Updates a State object: PUT /api/v1/states/<state_id>
    If the state_id is not linked to any State object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP body request to a dictionary
    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    Update the State object with all key-value pairs of the dictionary.
    Ignore keys: id, created_at and updated_at
    Returns the State object with the status code 200
    """
    state = storage.get('State', state_id)
    if not state:
        abort(404)
    else:
        if request.is_json:
            data = request.get_json()
            ignore_keys = ['id', 'created_at', 'updated_at']

            for key, value in data.items():
                if key not in ignore_keys:
                    setattr(state, key, value)
            state.save()
            return jsonify(state.to_dict()), 200
        abort(400, 'Not a JSON')
