#!/usr/bin/python3
''' Let's create a City view'''

from flask import Flask , abort , request
from api.v1.views import app_views
from os import name
from models.state import State
from models.city import City



app = Flask(__name__)


@app.route('/api/v1/states/<state_id>/cities', methods=['GET'])
def get_cities_by_state(state_id):
    """
    Retrieves the list of all City objects for a specific State.
    """
    state = State.find(state_id)
    if not state:
        abort(404)
    cities = City.all(state_id)
    return jsonify([city.to_dict() for city in cities])


@app.route('/api/v1/cities/<city_id>', methods=['GET'])
def get_city_by_id(city_id):
    """
    Retrieves a City object by its ID.
    """
    city = City.find(city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict()), 200


@app.route('/api/v1/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object by its ID.
    """
    city = City.find(city_id)
    if not city:
        abort(404)
    city.delete()
    return jsonify({}), 200


@app.route('/api/v1/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """
    Creates a new City object for a specific State.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    if 'name' not in data:
        abort(400, {'error': 'Missing name'})
    state = State.find(state_id)
    if not state:
        abort(404)
    city = City(name=data['name'], state_id=state_id)
    city.save()
    return jsonify(city.to_dict()), 201


@app.route('/api/v1/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """
    Updates a City object by its ID.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    city = City.find(city_id)
    if not city:
        abort(404)
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
