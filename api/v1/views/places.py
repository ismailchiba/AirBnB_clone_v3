#!/usr/bin/python3
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_places(city_id):
    """Retrieves the list of all Place objects"""
    city_by_id = storage.get(City, city_id)
    if not city_by_id:
        abort(404)

    place_list = [place.to_dict() for place in city_by_id.places]
    return make_response(jsonify(place_list), 200)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place(place_id):
    """Retrieves a Place object"""
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if place:
        place.delete()
        place.save()
        return jsonify({})
    abort(404)


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def create_place(city_id):
    """Creates a Place"""
    if city_id is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'name' not in data:
        return make_response(jsonify({'error': 'Missing name'}), 400)
    user_id = storage.get(User, data.get('user_id'))
    if not user_id:
        abort(404)
    city_id = data.get('city_id')
    Place = Place(**data)
    Place.save()
    return make_response(jsonify(Place.to_dict()), 201)

