#!/usr/bin/python3
"""Module for the new view of City objects"""


from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes city based on its id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a new city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    name = data.get('name')
    if not name:
        abort(400, 'Missing name')
    data['state_id'] = state_id
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates the city object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, 'Not a JSON')
    for k, v in data.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    storage.save()
    return jsonify(city.to_dict()), 200
