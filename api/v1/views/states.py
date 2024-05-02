#!/usr/bin/python3

"""Interact with the State model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.state import State
from models.base_model import BaseModel as BM


states = F(__name__)


@AV.route('/states', methods=['GET', 'POST'])
def get_or_create_states():
    """Get all states / Create a new state w no Id"""
    if RQ.method == 'GET':
        States = storage.all('State')
        response = [sstate.to_dict() for sstate in States.values()]
        status = 200
    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') is None:
            abort(400, 'Missing name')
        new_state = State(**RQ_json)
        new_state.save()
        response = new_state.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/states/<state_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_state(state_id):
    """Get, delete or update a State object w a given identifier"""
    response = {}
    if RQ.method == 'GET':
        response = storage.get('State', state_id)
        if response is None:
            abort(404, "Not found")
        status = 200
    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        sstate = storage.get('State', state_id)
        sstate = BM.db_update(RQ_json)
        response = sstate
        status = 200
    if RQ.method == 'DELETE':
        sstate = storage.get('State', state_id)
        if sstate is None:
            pass
        sstate.delete()
        del sstate
        response = {}
        status = 200
    return jsonify(response), status
