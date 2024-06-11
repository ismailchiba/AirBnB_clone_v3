#!/usr/bin/python3
"""
Handles city API
"""
from api.v1.views import app_views
from models.city import City
from models import storage
from flask import jsonify, request, abort
from models.state import State

@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def all_cities(state_id):
    """GET method for all cities in a specific state"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    city_list = [city.to_dict() for city in storage.all(City).values()
                 if city.state_id == state_id]
    return jsonify(city_list)

@app_views.route('/api/v1/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    """Get method for a specific city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/api/v1/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """POST method to create a city"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)

    new_data = request.get_json()
    if not new_data:
        abort(400, description="Not a JSON")
    if 'name' not in new_data:
        abort(400, description="Missing name")

    city = City(**new_data)
    city.state_id = state_id
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201

@app_views.route('/api/v1/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a particular city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>', methods=['PUT'])
def updates_city(city_id):
    '''Updates a City object'''
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    city_obj[0]['name'] = request.json['name']
    for obj in all_cities:
        if obj.id == city_id:
            obj.name = request.json['name']
    storage.save()
    return jsonify(city_obj[0]), 200
