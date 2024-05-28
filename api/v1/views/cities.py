#!/usr/bin/python3
"""Create new view for city objects that handles all default
RESTfull API actions
"""
from flask import Flask,jsonify, request, abort
from api.v1.views import app_views
from models import storage, State, City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_state_cities(state_id):
    state = storageget(State, state_id)
    if state is None:
        abort(400)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/state/<state_id>/cities', mrthods=['POST'])
def create_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if "name" not in data:
        abort(400, "Missing name")
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods["PUT"])
def city_update(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'update_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({})

