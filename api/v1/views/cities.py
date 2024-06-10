#!/usr/bin/python3
"""
Modeule for a New View For City
"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """
    Retrieves the list of all State objects
    """
    list_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        for obj in state.cities:
            list_cities.append(obj.to_dict())
        return (jsonify(list_cities))


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        return (jsonify(city.to_dict()))


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """
    Deletes a City object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a New City
    """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json:
        abort(400, description='Not a JSON')
    try:
        json_data = request.get_json()
    except Exception:
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    else:
        data = request.get_json().get('name')
        # initialize name like this directly
        obj = City(name=data, state_id=state_id)
        storage.new(obj)
        storage.save()
        return (jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """
    Updates a State object
    """
    city = storage.get(City, city_id)
    if city:
        if not request.get_json:
            abort(400, description='Not a JSON')
        try:
            json_data = request.get_json()
        except Exception:
            abort(400, description='Not a JSON')
        data = request.get_json()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at']:
                setattr(city, key, value)
                city.save()
        return (jsonify(city.to_dict()))
    else:
        abort(404)
