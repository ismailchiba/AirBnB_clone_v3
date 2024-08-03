#!/usr/bin/python3
""" API endpoints for places """

from models import storage
from models.city import City
from models.place import Place
from models.user import User
from flask import jsonify, abort, request
from api.v1.views import app_views

PLACES_SEGMENT = 'places'


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route(f'/{PLACES_SEGMENT}/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(f'/{PLACES_SEGMENT}/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """Deletes a Place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """Creates a new Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in data:
        return jsonify({'error': 'Missing user_id'}), 400
    if 'name' not in data:
        return jsonify({'error': 'Missing name'}), 400

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route(f'/{PLACES_SEGMENT}/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        return jsonify({'error': 'Not a JSON'}), 400

    forbidden_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in forbidden_keys:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200

