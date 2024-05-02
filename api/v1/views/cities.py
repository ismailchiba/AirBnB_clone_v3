#!/usr/bin/python3
"""
city objects that handles all default RESTFul API actions
"""
from flask import jsonify, request, abort
from models.state import State
from models.city import City
from api.v1.views import app_views
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def get_cities_in_state(state_id):
    """Gets all cities in specified state, using the states id"""
    state = storage.get(State, state_id)
    get_city = []
    if not state:
        return abort(404)
    for city in state.get_city:
        get_city.append(city.to_dict())
    return jsonify(get_city)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def get_city(city_id):
    """Gets a city using the city id"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        return abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """deletes a city using the city id"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        return abort(404)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """creates a city using the state id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    state = storage.get(State, state_id)
    if not state:
        return abort(404)
    if not request.get_json():
        return abort(400, 'Not a JSON')
    get_data = request.get_json()
    if 'name' not in get_data:
        return abort(400, 'Missing name')
    get_data['state_id'] = state_id

    city = City(**get_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """updates a city using the state id"""
    if request.content_type != 'application/json':
        return abort(400, 'Not a JSON')
    city = storage.get(City, city_id)
    if city:
        if not request.get_json():
            return abort(400, "Not a JSON")
        get_data = request.get_json()
        not_key = ['id', 'created_at', 'updated_at']

        for k, v in get_data.items():
            if k not in not_key:
                setattr(city, k, v)
            city.save()
            return jsonify(city.to_dict()), 200
        else:
            return abort(404)
