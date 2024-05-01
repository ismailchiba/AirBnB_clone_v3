#!/usr/bin/python3
"""
route for handling City objects and operations
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request, make_response
import json
from models.city import City
from models.state import State
from werkzeug.exceptions import BadRequest


@app_views.route(
    "/states/<state_id>/cities", methods=["GET"], strict_slashes=False
)
def city_by_state(state_id):
    """
    Retrieve all City objects from a specific State.

    Args:
        state_id (str): The unique identifier of the State.

    Returns:
        Response: A JSON-formatted list of cities
        belonging to the specified State,
        or a 404 error if the State is not found.
    """
    cities_by_state = []
    state = storage.get(State, state_id)

    if state is None:
        abort(404)
    for obj in state.cities:
        cities_by_state.append(obj.to_dict())

    return jsonify(cities_by_state)


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def city_by_id(city_id):
    """
    Retrieve a specific City object by its ID.

    Args:
        city_id (str): The unique identifier of the City object.

    Returns:
        Response: A JSON-formatted of the City object with the specified ID,
        or an error message if not found.
    """
    city = storage.get(City, str(city_id))

    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Delete a City object by its ID.

    Args:
        city_id (str): The unique identifier of the City object to delete.

    Returns:
        JSON: An empty json and a 200 status code
        if the deletion was successful,
        or a 404 status code if the City object was not found.
    """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({})


@app_views.route(
    "/states/<state_id>/cities", methods=["POST"], strict_slashes=False
)
def create_city(state_id):
    """
    Create a new City object associated with a State.
    Args:
        state_id (str): The unique identifier
        of the State for which a new City will be created.
    Returns:
       Response: A JSON-formatted representation of the
       newly created City object,
        or an error message if the creation fails.
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    try:
        city = request.get_json(silent=True)
        if "name" not in city:
            abort(400, "Missing name")
    except BadRequest:
        abort(400, "Not a JSON")

    city["state_id"] = state_id
    new_city = City(**city)
    new_city.save()
    res = jsonify(new_city.to_dict())
    return make_response(res, 201)


@app_views.route("cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Create a new City object associated with a State.

    Args:
        state_id (str): The unique identifier
        of the State for which a new City will be created.
    Returns:
        Response: A JSON-formatted  representation of
        the newly created City object,
        or an error message if the creation fails.
    """
    city = storage.get(City, str(city_id))
    if city is None:
        abort(404)
    try:
        data = request.get_json(silent=True)
    except BadRequest:
        abort(400, "Not a JSON")

    keys_ignored = ["id", "created_at", "updated_at", "state_id"]
    for key, val in data.items():
        if key not in keys_ignored:
            setattr(city, key, val)
    storage.save()
    res = jsonify(city.to_dict())
    return make_response(res, 200)
