#!/usr/bin/python3
"""handle State operations"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_state():
    """retrieves all State objects"""
    all_state = storage.all("State")
    state_list = []
    for obj in all_state.values():
        state_list.append(obj.to_json())
    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """return: newly created state obj"""
    state = request.get_json(silent=True)
    if state is None:
        abort(400, 'Not a JSON')
    if "name" not in state:
        abort(400, 'Name missing')

    new_state = State(**state)
    new_state.save()
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_id(state_id):
    """get state by the use of its id"""

    fetched_obj = storage.get("State", str(state_id))

    if fetched_obj is None:
        abort(404)

    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def put_state(state_id):
    """updates state"""
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400)
    state_obj = storage.get("State", str(state_id))
    if state_obj is None:
        abort(404)
    for key, values in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state_obj, key, values)
    state_obj.save()
    return jsonify(state_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"], strict_slashes=False)
def state_delete_by_id(state_id):
    """deletes State using its id"""

    state_obj = storage.get("State", str(state_id))

    if not state_obj:
        abort(404)

    storage.delete(state_obj)
    storage.save()

    return jsonify({})
