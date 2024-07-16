#!/usr/bin/python3
"""this file adds HTTP methods for the Place class"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.place import Place
from models.city import City
from models.user import User



@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_cities_place(city_id):
    """Gets a list of all cities of a specific state"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404, description="City not found")

    places = []
    for place in city.places:
        places.append(place.to_dict()) in city.places
    return jsonify(places)

@app_views.route('/places/<place_id>', methods=['GET'],
                  strict_slashes=False)
def get_place(place_id):
    """Retrieves a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())

@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """Deletes a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200

@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Creates a new Place under a specific City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_place = User(**data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201

@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200

if __name__ == '__main__':
    app_views.run(debug=True)
