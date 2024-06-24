#!/usr/bin/python3
""" views for City object """

from flask import jsonify, request, abort, make_response
from models import storage
from datetime import datetime
from models.city import City
from models.state import State
from api.v1.views import app_views


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_all_cities(state_id):
    """ Retrieve all cities object """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    list_cities = []
    for obj in state.cities:
        list_cities.append(obj.to_dict())
    return jsonify(list_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """ Retrieves a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """ Delete a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """ Create a new city """
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    if 'name' not in response:
        abort(400, 'Missing name')
    new_city = City(**response)
    new_city.state_id = state_id
    new_city.save()
    return make_response(jsonify(new_city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a city """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in keys:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)
