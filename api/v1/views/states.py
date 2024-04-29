#!/usr/bin/python3
"""states module"""
from flask import jsonify, abort, request, make_response
from api.v1.views.index import app_views
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def ret_stat():
    """Retrieves the list of all State objects"""
    all_states = [x.to_dict() for x in storage.all("State").values()]
    if not all_states:
        return jsonify({})
    return jsonify(all_states)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['GET'])
def get_stat(state_id):
    """Retrieves a State object"""
    s = storage.get(State, state_id)
    if s:
        return jsonify(s.to_dict())
    abort(404)


@app_views.route('/states/<state_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_stat(state_id):
        """Deletes a State object"""
        s = storage.get(State, state_id)
        if s:
            s.delete()
            storage.save()
            return jsonify({})
        abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_stat(state_id):
    """Update states"""
    if not state_id:
        abort(404)
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    resp_body = request.get_json(silent=True)
    if not resp_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for k, v in dict(resp_body).items():
        if k == "id" or k == "created_at" or k == "updated_at":
            continue
        setattr(s, k, v)
    storage.save()
    return jsonify(s.to_dict())


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_stat():
    """Create a new state"""
    resp_body = request.get_json(silent=True)
    if not resp_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in resp_body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = State(**resp_body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)
