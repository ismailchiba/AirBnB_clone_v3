#!/usr/bin/python3
"""
Modeule for a New View For State
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    list_states = []
    for obj in storage.all().values():
        if isinstance(obj, State):
            list_states.append(obj.to_dict())
    return (jsonify(list_states))


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """Retrieves a State object based on id"""
    state = storage.get(State, state_id)
    if state:
        return (jsonify(state.to_dict()))
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def state_del(state_id):
    """Deletes a State object based on id"""
    state = storage.get(State, state_id)
    if state:
        # delete all cities related to state
        # as state_id column in city table set to NOT NULL
        # and it cannot be empty
        for city in storage.all(City).values():
            if city.state_id == state_id:
                storage.delete(city)
        storage.delete(state)
        storage.save()
        return(jsonify({}))
    else:
        abort(404)


@app_views.route('/states', methods=['POST'],
                 strict_slashes=False)
def new_state():
    """create a new state"""
    if not request.get_json:
        abort(400, description='Not a JSON')
    try:
        json_data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    else:
        data = request.get_json().get('name')
        # initialize name like this directly
        obj = State(name=data)
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if state:
        if not request.get_json:
            abort(400, description='Not a JSON')
        try:
            json_data = request.get_json()
        except Exception:
            abort(400, description='Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(state, key, value)
                state.save()
        return (jsonify(state.to_dict()))
    else:
        abort(404)
