#!usr/bin/python3
"""
Creates new view for City obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City

@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """
    Retrieves a list of all cities in specified state
    """
    state_obj = storage.get("State", state_id)
    if not state_obj:
        abort(404)
    cities = [city.to_dict() for city in state_obj.cities]
    return jsonify(cities)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    """
    Retrieves a specific city by ID
    """
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    return jsonify(city_obj.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """
    Deletes a specific city by ID
    """
    city_obj = storage.get("City", city_id)
    if not city_obj:
        abort(404)
    storage.delete(city_obj)
    return jsonify({}), 200

@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city(state_id):
    """
    Creates a new city
    """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    city = City(**request.get_json())
    city.state_id = state.id
    city.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """
    Updates a specific city by ID
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
