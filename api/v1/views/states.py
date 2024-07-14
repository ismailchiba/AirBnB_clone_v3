#!/usr/bin/python3
"""
Creates new view for State obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, request, abort
from models.state import State
from models import storage
import json


@app_views.route('/api/v1/states', methods=['GET'])
def get_all_states():
    states = State.query.all()
    state_list = [state.to_dict() for state in states]
    return jsonify(state_list)


@app_views.route('/api/v1/states/<int:state_id>', methods=['GET'])
def get_state_by_id(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/api/v1/states/<int:state_id>', methods=['DELETE'])
def delete_state(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    state.delete()
    return jsonify({}), 200


@app_views.route('/api/v1/states', methods=['POST'])
def create_state():
    data = request.get_json()
    if not data or 'name' not in data:
        abort(400)
    new_state = State(name=data['name'])
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/api/v1/states/<int:state_id>', methods=['PUT'])
def update_state(state_id):
    state = State.query.get(state_id)
    if not state:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400)
    state.name = data.get('name', state.name)
    state.save()
    return jsonify(state.to_dict()), 200
