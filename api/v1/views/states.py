#!/usr/bin/python3
""" new view for State objects that handles all default RESTFul API actions: get, put and post """

from flask import jsonify, request
from models.state import State
from api.v1.views import app_views
from models import storage


@app_views.route('/States', methods['GET'])
def get_state():
     """ get all by id """
    states = storage.all(State).values()
    for state in states:
        return jsonify([state.to_dict()])


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state(state_id):
     """ get state by id"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(state.to_dict())


@app_views.route('states/<state_id>', method=[DELETE])
def del_state(state_id):
    """ delete state by id"""
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    storage.delete(state)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'])
def create_state():
    """ create new instance """
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400
    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ update """
    state = storage.get(State, state_id)
    if state is None:
        return jsonify({"error": "Not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.to_dict()), 200
