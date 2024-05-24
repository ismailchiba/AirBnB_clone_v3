#!/usr/bin/python3
"""
defines api for accessing city objects
"""
from flask import jsonify, abort, request
from . import app_views
from models.city import City
from models.state import State
from models import storage


@app_views.route('states/<state_id>/cities', methods=['GET'])
@app_views.route('states/<state_id>/cities/', methods=['GET'])
def get_state_cities(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city_obj(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city_obj(city_id):
    """Deletes a City object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('states/<state_id>/cities', methods=['POST'])
@app_views.route('states/<state_id>/cities/', methods=['POST'])
def create_state_city_obj(state_id):
    """ Creates a city object"""
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not data['state_id']:
        city = City(**data, state_id=state_id)
        storage.new(city)
    else:
        city = City(**data)
        storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    for key, val in data.items():
        if hasattr(city, key):
            setattr(city, key, val)
    storage.save()
    return jsonify(city.to_dict()), 200
