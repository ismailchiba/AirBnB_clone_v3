#!/usr/bin/python3

from flask import abort, jsonify, request

from api.v1.views import app_views, storage

# from models import storage
from models.state import State


@app_views.route("/states", methods=["GET"], strict_slashes=False)
def get_all_state():
    """Return all states"""
    states_list = []
    states_obj = storage.all(State)

    for obj in states_obj.values():
        states_list.append(obj.to_dict())

    response = jsonify(states_list), 200

    return response


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def get_state_by_id(state_id):
    """
    Retrieve a state by its ID.

    Args:
        state_id (str): The ID of the state to retrieve.

    Returns:
        tuple: A tuple containing the JSON representation
        of the state and the HTTP status code.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(State, str(state_id)).to_dict()

    if state is None:
        abort(404)

    response = jsonify(state), 200

    return response


@app_views.route("/states/<st_id>", methods=["DELETE"], strict_slashes=False)
def delete_state(st_id):
    """
    Delete a state by its ID.

    Args:
        st_id (str): The ID of the state to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(State, str(st_id))

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({})


@app_views.route("/states", methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create a new state.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new state and the HTTP status code 201.
    """
    # Get the JSON data from the request body
    body = request.get_json()

    # Check if the request body is empty or not in JSON format
    if body is None:
        abort(400, "Not a JSON")

    # Check if the 'name' key is present in the request body
    if "name" not in body:
        abort(400, "Missing name")

    # Create a new State object using the data from the request body
    new_state = State(**body)

    # Save the new state object to the database
    new_state.save()

    # Create a JSON response containing the data of the new state
    response = jsonify(new_state.to_dict()), 201

    return response
