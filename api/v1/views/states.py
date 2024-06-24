#!/usr/bin/python3
"""
create a new view for State objects that handles all default RESTful API
actions
"""
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request, g
from models.state import State


@app_views.route('/states', methods=['GET', 'POST'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def all_states(state_id=None):
    """list of all or given state_id State Objects"""
    state_dict = storage.all(State)
    state_instances = [val.to_dict() for val in state_dict.values()]
    if not state_id:
        if request.method == 'GET':
            return make_response(jsonify(state_instances), 200)

        elif request.method == 'POST':
            if not request.is_json or not request.get_json().get('name', None):
                abort(400)
            data = request.get_json()
            new_inst = State(**data)
            new_inst.save()
            data = storage.get("State", new_inst.id).to_dict()
            return make_response(jsonify(data), 201)

        elif request.method == 'HEAD':
            return make_response(jsonify(""), 200)

    obj_inst = storage.get('State', state_id)
    if not obj_inst:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(obj_inst.to_dict()), 200)

    elif request.method == 'DELETE':
        obj_inst.delete()
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400)
        data = request.get_json()
        for key in data.keys():
            if key not in ['id', 'created_at', 'update_id']:
                setattr(obj_inst, key, data[key])
        obj_inst.save()
        return make_response(jsonify(obj_inst.to_dict()), 200)

    elif request.method == 'HEAD':
        return make_response(jsonify(""), 200)
