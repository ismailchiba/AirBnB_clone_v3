#!/usr/bin/python3

from flask import abort, jsonify, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_state_cities(state_id):
    """
    Retrieve all cities associated with a given state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        tuple: A tuple containing a JSON response with the list of cities and a status code.
    """
    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())

    response = jsonify(city_list), 200

    return response


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    Retrieve a specific city by its ID.

    Args:
        city_id (str): The ID of the city to retrieve.

    Returns:
        tuple: A tuple containing the JSON representation of
        the city and the HTTP status code.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(City, str(city_id)).to_dict()

    if city is None:
        abort(404)

    response = jsonify(city), 200

    return response


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a city by its ID.

    Args:
        city_id (str): The ID of the city to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    city = storage.get(City, str(city_id))

    if city is None:
        abort(404)

    storage.delete(city)
    storage.save()

    return jsonify({})


# @app_views.route("/states/<st_id>", methods=["DELETE"], strict_slashes=False)
# def delete_state(st_id):
#     """
#     Delete a state by its ID.

#     Args:
#         st_id (str): The ID of the state to delete.

#     Returns:
#         tuple: An empty dictionary and the HTTP status code 200.

#     Raises:
#         404: If the state with the specified ID does not exist.
#     """
#     state = storage.get(State, str(st_id))

#     if state is None:
#         abort(404)

#     storage.delete(state)
#     storage.save()

#     return jsonify({})


# @app_views.route("/states", methods=["POST"], strict_slashes=False)
# def create_state():
#     """
#     Create a new state.

#     Returns:
#         tuple: A tuple containing the JSON representation
#         of the new state and the HTTP status code 201.
#     """
#     # Get the JSON data from the request body
#     body = request.get_json()

#     # Check if the request body is empty or not in JSON format
#     if body is None:
#         abort(400, "Not a JSON")

#     # Check if the 'name' key is present in the request body
#     if "name" not in body:
#         abort(400, "Missing name")

#     # Create a new State object using the data from the request body
#     new_state = State(**body)

#     # Save the new state object to the database
#     new_state.save()

#     # Create a JSON response containing the data of the new state
#     response = jsonify(new_state.to_dict()), 201

#     return response


# @app_views.route("/states/<state_id>", methods=["PUT"], strict_slashes=False)
# def update_state(state_id):
#     """
#     Update a state by its ID.

#     Args:
#         state_id (str): The ID of the state to update.

#     Returns:
#         tuple: A tuple containing the JSON representation
#         of the updated state and the HTTP status code 200.

#     Raises:
#         404: If the state with the specified ID does not exist.
#     """
#     # Get the JSON data from the request body
#     body = request.get_json()

#     # Check if the request body is empty or not in JSON format
#     if body is None:
#         abort(400, "Not a JSON")

#     # Get the state object from the database
#     state = storage.get(State, str(state_id))

#     # Check if the state object exists
#     if state is None:
#         abort(404)

#     # Update the state object with the data from the request body
#     for key, value in body.items():
#         if key not in ["id", "created_at", "updated_at"]:
#             setattr(state, key, value)

#     # Save the updated state object to the database
#     state.save()

#     # Create a JSON response containing the data of the updated state
#     response = jsonify(state.to_dict()), 200

#     return response
