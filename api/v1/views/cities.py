#!/usr/bin/python3
"""cities module"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete city single"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """create a city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'name' not in request_data:
        abort(400, "Missing name")
    request_data['state_id'] = state_id
    new_city = City(**request_data)
    storage.new(new_city)
    storage.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """update a single city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
