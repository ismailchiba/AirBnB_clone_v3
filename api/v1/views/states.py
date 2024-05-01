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
    if not state_id:
        abort(404)
    s = storage.get(State, state_id)
    if s:
        s.delete()
        storage.save()
        return (jsonify({}), 200)
    abort(404)


@app_views.route('/states/<state_id>', strict_slashes=False, methods=['PUT'])
def update_stat(state_id):
    """Updates a State object"""
    if not state_id:
        abort(404)
    s = storage.get(State, state_id)
    if not s:
        abort(404)
    res_body = request.get_json(silent=True)
    if not res_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    for key, value in res_body.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(s, key, value)
    storage.save()
    return jsonify(s.to_dict())

    # if not state_id:
    #     abort(404)
    # s = storage.get(State, state_id)
    # if not s:
    #     abort(404)
    # res_body = request.get_json(silent=True)
    # if not res_body:
    #     return make_response(jsonify({"error": "Not a JSON"}), 400)
    # setattr(s, 'name', res_body.get('name'))
    # storage.save()
    # return jsonify(s.to_dict(), 200)


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_stat():
    """Create a new state"""
    res_body = request.get_json(silent=True)
    if not res_body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'name' not in res_body:
        return make_response(jsonify({"error": "Missing name"}), 400)
    obj = State(**res_body)
    obj.save()
    return make_response(jsonify(obj.to_dict()), 201)

    # res_body = request.get_json(silent=True)
    # if not res_body:
    #     return make_response(jsonify({"error": "Not a JSON"}), 400)
    # if 'name' not in res_body:
    #     return make_response(jsonify({"error": "Missing name"}), 400)
    # obj = State(**res_body)
    # obj.save()
    # return make_response(jsonify(obj.to_dict()), 201)
