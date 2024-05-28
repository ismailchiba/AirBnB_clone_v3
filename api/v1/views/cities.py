#!/usr/bin/python3
"""Cities view for API v1."""
from flask import abort, jsonify, request
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrieve the list of all City objects of a State. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieve a City object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Create a City in a State. """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, "Not a JSON")
    if 'name' not in json_data:
        abort(400, "Missing name")
    city = City(**request.get_json())
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Update a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    json_data = request.get_json(silent=True)
    if json_data is None:
        abort(400, "Not a JSON")
    ignore_keys = ["id", "state_id", "created_at", "updated_at"]
    for key, value in request.get_json().items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Delete a City object. """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200
