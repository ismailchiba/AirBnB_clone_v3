#!/usr/bin/python3

from flask import Blueprint, jsonify, abort, request, make_response
from werkzeug.exceptions import BadRequest
from models import storage
from models.state import State

app_states = Blueprint("app_states", __name__)


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_states.route("/", methods=['GET'])
def retrive_all_states():
    """ This function return list of all states """
    return [obj.to_dict() for _, obj in storage.all(State).items()]


@app_states.route("/<state_id>", methods=['GET'])
def retrive_state(state_id):
    """ This function is used to retrive a specific state
        object using its id
    """
    state = get_object_by_id(State, state_id)
    if not state:
        abort(404)
    return state.to_dict()


@app_states.route("/<state_id>", methods=['DELETE'])
def delete_state(state_id):
    """ This function is used to delete an state object when
        the DELETE method is called
    """
    state = get_object_by_id(State, state_id)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return {}, 200


@app_states.route("/", methods=['POST'])
def create_state():
    """ This function creates a new state object
    """
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_state = State()
    new_state.name = request_data.get('name')
    new_state.save()
    return new_state.to_dict(), 201


@app_states.route("/<state_id>", methods=['PUT'])
def update_state(state_id):
    """ This function updates an existing state object
    """
    state = get_object_by_id(State, state_id)
    if not state:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)
    state.save()
    return state.to_dict(), 200
