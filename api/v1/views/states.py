#!/usr/bin/python3
"""
route for handling State objs and ops
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    retrieves all State objects
    """
    state_list = []
    state_object = storage.all("State")
    for obj in state_object.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    create state route
    return newly created state obj
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    if "name" not in state_json:
        abort(400, 'Missing name')

    new_state = State(**state_json)
    new_state.save()
    response = jsonify(new_state.to_json())
    response.status_code = 201

    return response


@app_views.route("/states/<state_id>",  methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    gets a specific State object by ID
    """

    fetched_object = storage.get("State", str(state_id))

    if fetched_object is None:
        abort(404)

    return jsonify(fetched_object.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def stateUpdate_by_id(state_id):
    """
    updates specific State object by ID
    state_id: state object ID
    """
    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_object = storage.get("State", str(state_id))
    if fetched_object is None:
        abort(404)
    for key, value in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_object, key, value)
    fetched_object.save()
    return jsonify(fetched_object.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    deletes State by id
    """

    fetched_object = storage.get("State", str(state_id))

    if fetched_object is None:
        abort(404)

    storage.delete(fetched_object)
    storage.save()

    return jsonify({})
