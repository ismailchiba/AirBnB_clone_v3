#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for City objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State

api_route_1 = "/states/<string:state_id>/cities"
api_route_2 = "/cities/<string:city_id>"


@app_views.route(api_route_1, methods=["GET"], strict_slashes=False)
def get_state_cities(state_id):
    """
    Retrieve all cities associated with a given state.

    Args:
        state_id (str): The ID of the state.

    Returns:
        tuple: A tuple containing a JSON response with the
        list of cities and a status code.
    """
    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    city_list = []
    for city in state.cities:
        city_list.append(city.to_dict())

    response = jsonify(city_list), 200

    return response


@app_views.route(api_route_2, methods=["GET"], strict_slashes=False)
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
    city = storage.get(City, str(city_id))

    if city is None:
        abort(404)

    response = jsonify(city.to_dict()), 200

    return response


@app_views.route(api_route_2, methods=["DELETE"], strict_slashes=False)
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


@app_views.route(api_route_1, methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Create a new state's city.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new city and the HTTP status code 201.
    """
    state = storage.get(State, str(state_id))

    if state is None:
        abort(404)

    body = request.get_json(silent=True)
    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if "name" not in body:
        return make_response(jsonify({"error": "Missing name"}), 400)

    body["state_id"] = state_id

    new_city = City(**body)

    new_city.save()

    response = jsonify(new_city.to_dict()), 201

    return response


@app_views.route(api_route_2, methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Update a city by its ID.

    Args:
        city_id (str): The ID of the city to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated city and the HTTP status code 200.

    Raises:
        404: If the city with the specified ID does not exist.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    city = storage.get(City, str(city_id))

    if city is None:
        abort(404)

    updated = False
    for key, value in body.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(city, key, value)
            updated = True

    if updated:
        storage.save()

    response = jsonify(city.to_dict()), 200

    return response
