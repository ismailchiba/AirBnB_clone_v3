#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for State objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views, storage
from models.state import State

api_route_1 = "/states"
api_route_2 = "/states/<string:state_id>"


@app_views.route(api_route_1, methods=["GET"], strict_slashes=False)
def get_all_state():
    """
    Return all states.

    This function retrieves all State objects from the storage
    and returns them in a JSON format.

    Returns:
        response (flask.Response): A JSON response with a list of
        all states and status code 200.
    """
    states_list = []
    states_obj = storage.all(State)

    for obj in states_obj.values():
        states_list.append(obj.to_dict())

    response = jsonify(states_list), 200

    return response


@app_views.route(api_route_2, methods=["GET"], strict_slashes=False)
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
    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    response = jsonify(state.to_dict()), 200

    return response


@app_views.route(api_route_2, methods=["DELETE"], strict_slashes=False)
def delete_state(state_id):
    """
    Delete a state by its ID.

    Args:
        state_id (str): The ID of the state to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    storage.delete(state)
    storage.save()

    return jsonify({}), 200


@app_views.route(api_route_1, methods=["POST"], strict_slashes=False)
def create_state():
    """
    Create a new state.

    This function creates a new State object from the JSON data in
    the request body and saves it to the storage.

    Returns:
        response (tuple): A tuple containing the JSON representation
        of the new state and the HTTP status code 201.

    Raises:
        400: If the request body is not JSON or if the 'name' key is missing.
    """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_state = State(**body)

    new_state.save()

    response = jsonify(new_state.to_dict()), 201

    return response


@app_views.route(api_route_2, methods=["PUT"], strict_slashes=False)
def update_state(state_id):
    """
    Update a state by its ID.

    Args:
        state_id (str): The ID of the state to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated state and the HTTP status code 200.

    Raises:
        404: If the state with the specified ID does not exist.
    """
    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    updated = False
    for key, value in body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(state, key, value)
            updated = True

    if updated:
        storage.save()

    response = jsonify(state.to_dict()), 200

    return response
