#!/usr/bin/python3
"""this file adds HTTP methods for the State model"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.city import City

@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    """Gets a List of all city"""
    cities = storage.all(City).values()
    cities_list = []
    for city in cities:
        cities_list.append(city.to_dict())
    return jsonify(cities_list)

@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Gets a specfic city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())

@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Deletes a specfic city with id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city():
    """Creates a specfic state with id"""
    data = request.get_json(force=True)
    if not data:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    
    new_city = City(**data)
    storage.new(new_city)
    storage.save()
    return make_response(jsonify(new_city.to_dict()), 201)

@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """Updates a specfic city with a id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True)
    if not data:
        abort(400, description='Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return make_response(jsonify(city.to_dict()), 200)

if __name__ == '__main__':
    app_views.run(debug=True)