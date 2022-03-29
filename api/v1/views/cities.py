#!/usr/bin/python3
""" API view for State objects. """
import os
import json
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def all_cities(state_id):
    """ Returns the list of cities in State obj in JSON. """
    city_list = []
    try:
        state = storage.get(State, state_id)["State.{}".format(state_id)]
    if not state:
        abort(404)
    all_cities = storage.all(City)
    for city in all_cities.values():
        if city.state_id == state_id:
            city_list.append(city.to_dict())
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """ Returns the City obj in JSON """
    try:
        city = storage.all(City)["City.{}".format(city_id)]
    except (TypeError, KeyError):
        abort(404)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """ Deletes the City obj from Storage. """
    try:
        city = storage.all(City)["City.{}".format(city_id)]
    except (TypeError, KeyError):
        abort(404)
    if not city:
        abort(404)
    deleted = {}
    storage.delete(city)
    storage.save()
    return jsonify(deleted), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """ Creates a City obj and saves to Storage. """
    try:
        state = storage.all(State)["State.{}".format(state_id)]
    except (TypeError, KeyError):
        abort(404)
    if not state:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in request.json:
            abort(400, {'message': 'Missing name'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    content['state_id'] = state_id
    new_city = City(**content)
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """ Updates a City obj to Storage. """
    try:
        city = storage.get(City, city_id)["City.{}".format(city_id)]
    except (TypeError, KeyError):
        abort(404)
    if not city:
        abort(404)
    content = request.get_json()
    try:
        json.dumps(content)
        if 'name' not in content:
            abort(400, {'message': 'Missing name'})
    except (TypeError, OverflowError):
        abort(400, {'message': 'Not a JSON'})
    ignored_keys = ['id', 'created_at', 'updated_at', 'state_id']
    for key, value in content.items():
        if key not in ignored_keys:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
