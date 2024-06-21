#!/usr/bin/python3
"""places module"""
from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """get all places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """get single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """delete places"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """create places"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'name' not in request_data:
        abort(400, "Missing name")
    request_data['city_id'] = city_id
    new_place = Place(**request_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """upadate many places"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
