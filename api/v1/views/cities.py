#!/usr/bin/python3
"""
city restful api
"""
from flask import jsonify
from flask import request
from flask import abort
from models.city import City
from models import storage
from models.state import State
from api.v1.views import app_views
import models
import re


@app_views.route('/states/<state_id>/cities/',
                 strict_slashes=False, methods=['GET'])
def get_all_cities(state_id):
    """get cities by state id"""
    states = storage.get(State, state_id)
    if states:
        cities = [city.to_dict() for city in states.cities]
        return jsonify(cities)
    return (abort(404))


@app_views.route('/cities/<city_id>/',
                 strict_slashes=False, methods=['GET'])
def get_citybyId(city_id):
    """retrieve city by city id"""
    cities = storage.all(City)
    for k, v in cities.items():
        if v.to_dict().get('id') == city_id:
            return jsonify(v.to_dict())
    return (abort(404))


@app_views.route('/states/<state_id>/cities/',
                 strict_slashes=False, methods=['POST'])
def post_city(state_id):
    """post a city for a certain state id"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    elif 'name' not in data.keys():
        return (abort(400, 'Missing name'))
    elif not data['name']:
        return (abort(400, 'Missing name'))
    else:
        if storage.get(State, state_id):
            city = City(**data)
            city.state_id = state_id
            storage.new(city)
            storage.save()
            return jsonify(city.to_dict()), 201
        else:
            return (abort(404))


@app_views.route('/cities/<city_id>/',
                 strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """update city in state"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    city = storage.get(City, city_id)
    if city is None:
        return (abort(404))
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(city, k, v)
    city.save()
    return jsonify(city.to_dict()), 200


@app_views.route('cities/<city_id>/',
                 strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """delete the city by its city id"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200
