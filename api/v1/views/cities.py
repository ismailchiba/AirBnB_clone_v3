#!/usr/bin/python3
"""states"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route(
    '/states/<state_id>/cities',
    methods=['GET'],
    strict_slashes=False
)
def get_cities(state_id):
    """gets all cities"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = [i.to_dict() for i in state.cities]
    return jsonify(all_cities)


@app_views.route(
    '/cities/<city_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_city(city_id):
    """git city from id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route(
    '/cities/<city_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_city(city_id):
    """delete city from id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
)
def create_city(state_id):
    """create city"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    if not request.get_json():
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    if 'name' not in request.get_json():
        return make_response(
            jsonify({"error": "Missing name"}), 400
        )
    city = request.get_json()
    i = City(**city)
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route(
    '/cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_city(city_id):
    """update city"""
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    for k, v in data.items():
        if k not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, k, v)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
