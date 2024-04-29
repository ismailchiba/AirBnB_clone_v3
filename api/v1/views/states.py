#!/usr/bin/python3

"""
View for State objects that handles all default RESTFul API actions
"""

from api.v1.views import app_views, storage
from flask import jsonify, abort, request
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieving all State objects

    Return: json of all states
    """

    state_list = []
    state_object = storage.all("State")
    for obj in state_object.values():
        state_list.append(obj.to_json())

    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Creating State routes

    Return: Newly created state obj
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
    Gets a specific State object by ID
        :state_id: State object ID

    Return: State obj with the specified ID or error
    """

    fetched_object = storage.get("State", str(state_id))

    if fetched_object is None:
        abort(404)

    return jsonify(fetched_object.to_json())


@app_views.route("/states/<state_id>",  methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Updating specific State object by ID
        :state_id: state object ID

    Return: State object and 200 on success, or 400 or 404 on failure
    """

    state_json = request.get_json(silent=True)
    if state_json is None:
        abort(400, 'Not a JSON')
    fetched_object = storage.get("State", str(state_id))
    if fetched_object is None:
        abort(404)
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_object, key, val)
    fetched_object.save()
    return jsonify(fetched_object.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Removes State by ID
        :state_id: State object ID

    Return: Empty dictionary with 200 or 404 if not found
    """

    fetched_object = storage.get("State", str(state_id))

    if fetched_object is None:
        abort(404)

    storage.delete(fetched_object)
    storage.save()

    return jsonify({})
