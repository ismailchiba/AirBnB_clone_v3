#!/usr/bin/python3
"""
Creates new view for Place obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route(
        '/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_place_by_city(city_id):
    """
    Retrieves a list of all places in specified city
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places_list = []
    places = city.places
    if not places:
        continue
    else:
        for place in places:
            places_list.append(place.to_dict())
    return jsonify(places_list)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a specific place by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a specific place by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """
    Creates a new place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)  # No valid user
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    storage.save()
    place_json = place.to_dict()
    return jsonify(place_json), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a specific place by ID
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
