#!/usr/bin/python3
""" this area is for learning purpose"""
from flask import jsonify, make_response, request, abort
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    """ retrive list of all states """
    st = storage.all(State).values()
    if st is None:
        abort(404)
    lst_state = [i.to_dict() for i in st]
    return jsonify(lst_state)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    """ get state by id """
    st_value = storage.get(State, state_id)
    if st_value is None:
        abort(404)
    return jsonify(st_value.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def rm_state(state_id):
    """ Deletes a State object"""
    st_value = storage.get(State, state_id)
    if st_value is None:
        abort(404)
    storage.delete(st_value)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def add_post():
    """ add or create a state"""
    if not request.get_json():
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in request.get_json():
        return make_response(jsonify({"error": "Missing name"}), 400)
    new_state = State(**request.get_json())
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def st_update(state_id):
    """ update state object"""

    st_id = storage.get(State, state_id)
    if st_id is None:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    for key, value in request.get_json().items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(st_id, key, val)
    st_id.save()
    return jsonify(st_id.to_dict()), 200
