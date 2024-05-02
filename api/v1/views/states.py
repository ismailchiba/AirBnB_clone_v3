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
    States = storage.all('State')
    if States is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
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
    sstate = storage.get('State', state_id)
    if sstate is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = sstate.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        sstate = State.db_update(RQ_json)
        sstate.save()   # type: ignore
        response = sstate.to_dict()    # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        sstate.delete()   # type: ignore
        del sstate
        status = 200
    return jsonify(response), status
