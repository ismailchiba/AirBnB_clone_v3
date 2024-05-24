#!/usr/bin/python3
"""
defines api for accessing city objects
"""
from flask import jsonify, abort, request
from . import app_views
from models.place import Place
from models.city import City
from models.user import User
from models import storage
from os import getenv


@app_views.route('cities/<city_id>/places', methods=['GET'])
@app_views.route('cities/<city_id>/places/', methods=['GET'])
def get_city_places(city_id):
    """
    Retrieves list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    places = []
    if not city:
        abort(404)
    for place in storage.all(Place).values():
        if place.city_id == city.id:
            places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place_obj(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place_obj(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('cities/<city_id>/places', methods=['POST'])
@app_views.route('cities/<city_id>/places/', methods=['POST'])
def create_city_place_obj(city_id):
    """ Creates a Place object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    if not data.get("city_id"):
        place = Place(**data, city_id=city_id)
        storage.new(place)
    else:
        place = Place(**data)
        storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place_obj(place_id):
    """
    Updates a Place object
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    for key, val in data.items():
        if hasattr(place, key):
            setattr(place, key, val)
    storage.save()
    return jsonify(place.to_dict()), 200
