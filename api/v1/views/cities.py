#!/usr/bin/python3
"""
This file handles all the default  RESTFul API
actions (CRUD)
"""

from flask import abort, jsonify, make_response, request
from models import storage
from models.city import City
from api.v1.views import app_views


@app_views.route('/states/<string:state_id>/cities',
                 methods=["GET"], strict_slashes=False)
def get_cities_of_state(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    state = storage.get("State", state_id)

    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<string:city_id>',
                 methods=["GET"], strict_slashes=False)
def get_city(city_id):
    """
    Retrieves a City object
    """
    city = storage.get("City", city_id)
    if city is not None:
        return jsonify(city.to_dict())
    abort(404)


@app_views.route('/cities/<string:city_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a City object with the specified city_id
    """
    city = storage.get("City", city_id)
    if city is not None:
        city.delete()
        storage.save()
        return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/states/<string:state_id>/cities', methods=["POST"],
                 strict_slashes=False)
def create_city(state_id):
    """
    Creates a City object
    """
    state = storage.get("State", state_id)
    if state is not None:
        request_body = request.get_json()
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        if 'name' not in request_body:
            return make_response(jsonify({'error': 'Missing name'}), 400)

        request_body['state_id'] = state_id
        new_city = City(**request_body)
        new_city.save()
        return make_response(jsonify(new_city.to_dict()), 201)
    abort(404)


@app_views.route('/cities/<city_id>',
                 methods=["PUT"], strict_slashes=False)
def update_city(city_id):
    """
    Updates a city object with the given city_id
    """
    city = storage.get("City", city_id)
    if city is not None:
        request_body = request.get_json()
        if not request.is_json:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for k, v in request_body.items():
            if k not in ["id", "state_id", "created_at", "updated_at"]:
                setattr(city, k, v)
        city.save()
        return jsonify(city.to_dict())
    abort(404)
