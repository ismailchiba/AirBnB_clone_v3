#!/usr/bin/python3
"""
Routes for handling City objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves all City objects from a specific state.
    """
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    city_list = [city.to_json() for city in state.cities]
    return jsonify(city_list)


@app_views.route("/states/<state_id>/cities", methods=["POST"], strict_slashes=False)
def create_city(state_id):
    """
    Creates a new City object.
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        abort(400, 'Not a JSON')

    state = storage.get("State", state_id)
    if not state:
        abort(404)

    if "name" not in city_json:
        abort(400, 'Missing name')

    city_json["state_id"] = state_id

    new_city = City(**city_json)
    new_city.save()
    return jsonify(new_city.to_json()), 201


@app_views.route("/cities/<city_id>", methods=["GET"], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a specific City object by ID.
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a specific City object by ID.
    """
    city_json = request.get_json(silent=True)
    if not city_json:
        abort(400, 'Not a JSON')

    city = storage.get("City", city_id)
    if not city:
        abort(404)

    for key, value in city_json.items():
        if key not in ["id", "created_at", "updated_at", "state_id"]:
            setattr(city, key, value)

    city.save()
    return jsonify(city.to_json())


@app_views.route("/cities/<city_id>", methods=["DELETE"], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object by ID.
    """
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    storage.delete(city)
    storage.save()
    return jsonify({}), 200
