#!/usr/bin/python3
"""
Route for handling State objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def state_get_all():
    """
    Retrieve all State objects

    :return: JSON of all states
    """
    # Initialize an empty list to store state objects
    state_list = []

    # Fetch all state objects from storage
    state_obj = storage.all("State")

    # Iterate over fetched state objects and add them to the list
    for obj in state_obj.values():
        state_list.append(obj.to_json())

    # Return the list of state objects as JSON
    return jsonify(state_list)


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def state_create():
    """
    Create a new State object

    :return: newly created state object
    """
    # Fetch JSON data from the request
    state_json = request.get_json(silent=True)

    # Check if the request is a valid JSON
    if state_json is None:
        abort(400, 'Not a JSON')

    # Check if the JSON data contains a name
    if "name" not in state_json:
        abort(400, 'Missing name')

    # Create a new State object using the JSON data
    new_state = State(**state_json)

    # Save the new state object to storage
    new_state.save()

    # Create a response with the newly created state object
    resp = jsonify(new_state.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def state_by_id(state_id):
    """
    Get a specific State object by ID

    :param state_id: state object ID
    :return: state object with the specified ID or error
    """
    # Fetch the state object from storage
    fetched_obj = storage.get("State", str(state_id))

    # Check if the state object exists
    if fetched_obj is None:
        abort(404)

    # Return the fetched state object as JSON
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
def state_put(state_id):
    """
    Update a specific State object by ID

    :param state_id: state object ID
    :return: state object and 200 on success, or 400 or 404 on failure
    """
    # Fetch JSON data from the request
    state_json = request.get_json(silent=True)

    # Check if the request is a valid JSON
    if state_json is None:
        abort(400, 'Not a JSON')

    # Fetch the state object from storage
    fetched_obj = storage.get("State", str(state_id))

    # Check if the state object exists
    if fetched_obj is None:
        abort(404)

    # Update the state object with the JSON data
    for key, val in state_json.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(fetched_obj, key, val)

    # Save the updated state object to storage
    fetched_obj.save()

    # Return the updated state object as JSON
    return jsonify(fetched_obj.to_json())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def state_delete_by_id(state_id):
    """
    Delete a State object by ID

    :param state_id: state object ID
    :return: empty dict with 200 or 404 if not found
    """
    # Fetch the state object from storage
    fetched_obj = storage.get("State", str(state_id))

    # Check if the state object exists
    if fetched_obj is None:
        abort(404)

    # Delete the state object from storage
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty dict as JSON
    return jsonify({})
