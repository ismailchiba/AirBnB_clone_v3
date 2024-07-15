#!/usr/bin/python3
"""this file adds HTTP methods for the State model"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """Gets a list of all cities of a specific state"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description="State not found")

    cities = []
    for city in state.cities:
        cities.append(city.to_dict())
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by its ID"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Deletes a specfic city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """Creates a new City object under a specific State"""
    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    # Check if state_id is linked to any State object
    state = storage.get(State, state_id)
    if state is None:
        abort(404, description="State not found")

    new_city = City(name=data['name'], state_id=state.id)
    storage.new(new_city)
    storage.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updates a city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")

    city.name = data.get('name', city.name)
    storage.save()

    return jsonify(city.to_dict()), 200


if __name__ == '__main__':
    app_views.run(debug=True)
