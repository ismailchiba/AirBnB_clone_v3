#!/usr/bin/python3
"""
This file defines the routes to perform operations
on the Place object
"""

from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects
    """

    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    places = [place.to_dict() for place in city.places]

    return jsonify(places)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a Place object with the specified place_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes  Place object with the specified place_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place object
    """

    city = storage.get("City", city_id)

    if city is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    if 'user_id' not in request_body:
        abort(400, description='Missing user_id')

    user = storage.get("user", request_body.get('user_id'))

    if user is None:
        abort(404)

    if 'name' not in request_body:
        abort(400, description='Missing name')

    request_body['city_id'] = city_id
    new_place = Place(**request_body)

    storage.new(new_place)
    storage.save()

    return make_response(new_place.to_dict(), 201)


@app_views.route('/places/<place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    This method updates Place object with the specified
    place_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    for key, value in request_body.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)

    place.save()

    return jsonify(place.to_dict())
