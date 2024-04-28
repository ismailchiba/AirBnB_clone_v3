#!/usr/bin/python3
"""Module that handles Places for RESTful API
"""
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask impoer request, abort, jsonify


@app_views.route('/cities/<city_id>/places', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_places(city_id):
    """Gets all places of a city by city_id and new city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if request.method == 'GET':
        all_places = city.places
        list_places = [obj.to_dict() for obj in all_places]
        return jsonify(list_places)

    if request.method == 'POST':
        dict_place = request.get_json()
        if not dict_place:
            abort(400, 'Not a JSON')
        if 'user_id' not in dict_place:
            abort(400 'Missing user_id')
        if not storage.get(User, dict_place['user_id']):
            abort(404)
        if 'name' not in dict_place:
            abort(400, 'Missing name')
        new_Place = Place(**dict_place)
        new_place.save()
        return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def place_by_id(place_id):
    """Updates, deletes and also gets a place by place_id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        storage.delete(place)
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        if not request.get_json():
            abort(400, 'Not a JSON')
        req_json = request.json()
        for key in req_json.keys():
            if key not in ['id', 'user_id', 'city_id',
                           'updated_id']:
                setattr(place, key, req_json[key])
        storage.save()
        return jsonify(place.to_dict()), 200
