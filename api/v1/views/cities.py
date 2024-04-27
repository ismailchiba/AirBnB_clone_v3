#!/usr/bin/python3
'''Handles City objects for RESTful API actions'''

import re
from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id):
    '''gets and creates objects of City object'''
    if request.method == 'GET':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    if request.method == 'POST':
        state = storage.get(State, state_id)
        if not state:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'name' not in body:
            abort(400, 'Missing name')
        # create city
        city = City(name=body['name'], state_id=state_id)
        storage.new(city)
        storage.save()
        return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def one_city(city_id):
    '''gets one City object'''
    if request.method == 'GET':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        city = storage.get(City, city_id)
        if not city:
            abort(404)
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        for key, value in body.items():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                city.__setattr__(key, value)
        storage.save()
        return jsonify(city.to_dict()), 200
