#!/usr/bin/python3
''' Let's create a Place view'''

from flask import Flask , abort , request
from api.v1.views import app_views
from os import name
from models.user import User
from models.place import Place
from models.state import State

app = Flask(__name__)

@app.route('/api/v1/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects for a specific City.
    """
    city = City.find(city_id)
    if not city:
        abort(404)
    places = Place.all(city_id)
    return jsonify([place.to_dict() for place in places])

@app.route('/api/v1/places/<place_id>', methods=['GET'])
def get_place_by_id(place_id):
    """
    Retrieves a Place object by its ID.
    """
    place = Place.find(place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict()), 200

@app.route('/api/v1/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object by its ID.
    """
    place = Place.find(place_id)
    if not place:
        abort(404)
    place.delete()
    return jsonify({}), 200

@app.route('/api/v1/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """
    Creates a new Place object for a specific City.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    if 'user_id' not in data or 'name' not in data:
        abort(400, {'error': 'Missing user_id or name'})
    city = City.find(city_id)
    if not city:
        abort(404)
    user = User.find(data['user_id'])
    if not user:
        abort(404)
    place = Place(name=data['name'], user_id=data['user_id'], city_id=city_id)
    place.save()
    return jsonify(place.to_dict()), 201

@app.route('/api/v1/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """
    Updates a Place object by its ID.
    """
    if not request.is_json:
        abort(400, {'error': 'Not a JSON'})
    data = request.get_json()
    place = Place.find(place_id)
    if not place:
        abort(404)
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
