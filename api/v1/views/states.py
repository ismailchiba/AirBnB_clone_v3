#!/usr/bin/python3
"""state"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_all_states():
    """get all state instances in storage"""
    state_list = [obj.to_dict() for obj in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route('/states/<string:state_id>', methods=['GET'],
                 strict_slashes=False)
def get_state(state_id):
    """
    get state with id

    Args:
    state_id: id of state tot get
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<string:state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """delete state with id

    Args:
    state_id: id of state to delete
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    """creates a new instance of State via POST"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    json_str = request.get_json()
    state_obj = State(**json_str)
    state_obj.save()
    return (jsonify(state_obj.to_dict()), 201)


@app_views.route('/states/<string:state_id>', methods=['PUT'],
                 strict_slashes=False)
def update_state(state_id):
    """updates a state object with id match via PUT"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    for key, val in request.get_json().items():
        if key not in ['id', 'created_at', 'updated']:
            setattr(state_obj, key, val)
    storage.save()
    return jsonify(obj.to_dict())
