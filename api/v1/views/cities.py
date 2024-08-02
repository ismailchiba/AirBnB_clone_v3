#!/usr/bin/python3
""" API endpoints for cities """

from models import storage
from models.state import State
from models.city import City

from flask import jsonify, abort, request

from api.v1.views import app_views

from api.v1.views.states import STATES_SEGMENT
CITIES_SEGMENT = 'cities'


@app_views.route(f'/{ STATES_SEGMENT }/<state_id>/{ CITIES_SEGMENT }',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Gets the list of all cities of a state id """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route(f'/{ CITIES_SEGMENT }/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Gets a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(f'/{ CITIES_SEGMENT }/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Deletes a city by id """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route(f'/{ STATES_SEGMENT }/<state_id>/{ CITIES_SEGMENT }',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """ Creates a city """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route(f'/{ CITIES_SEGMENT }/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    forbidden_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(city, key, value)
    city.save()

    return jsonify(city.to_dict()), 200
