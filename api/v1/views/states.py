#!/usr/bin/python3
""" RESTFul API - State """

from api.v1.views import app_views
from flask import Flask
from models import storage
from models.state import State
from models.city import City
from flask import jsonify, request, abort


@app_views.route('/states/', methods=['GET'], strict_slashes=False)
def retrieve_list_all_states():
    """ Retrieves the list of all State objects: GET /api/v1/states """
    if request.method == 'GET':
        list_all_storage = []
        for st in storage.all(State).values():
            list_all_storage.append(st.to_dict())
        return jsonify(list_all_storage)


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_state(state_id):
    """ Retrieves a State object: GET /api/v1/states/<state_id> """
    if request.method == 'GET':
        if storage.get(State, state_id) is not None:
            return jsonify(storage.get(State, state_id).to_dict())
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_state(state_id):
    """ Deletes a State object:: DELETE /api/v1/states/<state_id> """
    if request.method == 'DELETE':
        if storage.get(State, state_id) is not None:
            storage.delete(storage.get(State, state_id))
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_new_state():
    """ Creates a State: POST /api/v1/states """
    if request.method == 'POST':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req_name = request.get_json()
        if 'name' not in dict_req_name:
            return jsonify('Missing name'), 400
        new_obj_State = State(**dict_req_name)
        new_obj_State.save()
        return jsonify(new_obj_State.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """ Updates a State object: PUT /api/v1/states/<state_id> """
    if request.method == 'PUT':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req = request.get_json()
        if storage.get(State, state_id) is not None:
            if 'name' in dict_req:
                storage.get(State, state_id).name = dict_req['name']
                storage.get(State, state_id).save()
                return jsonify(storage.get(State, state_id).to_dict()), 200
        abort(404)
