#!/usr/bin/python3
"""
The view for Place objects that handles all default
RESTFul API actions
"""

from flask import jsonify, make_response, request, abort
from models import storage
from models.place import Place
from api.v1.views import app_views



@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def get_places(city_id):
    """
    This method retrieves list of all Place ofjects of a
    City specified with city_id
    """

    city = storage.get("City", city_id)

    if city is not None:
        all_places = storage.all("Place")

        places_obj = []

        for value in all_places.values():
            if value.city_id == city_id:
                places_obj.append(value.to_dict())

        return jsonify(places_obj)

    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def get_place(place_id):
    """
    This method retrieves a Place object
    """

    place = storage.get(Place, place_id)

    if place is not None:
        return jsonify(place.to_dict())

    abort(404)


@app_views.route('/places/<place_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    This method deletes a Place object with the specified
    place_id
    """

    place = storage.get("Place", place_id)

    if place is not None:
        storage.delete(place)
        storage.save()

        return make_response({}, 200)

    abort(404)


@app_views.route('/cities/<city_id>/places',
                 methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    This method creates a new Place object on the City specified by
    the city_id
    """

    city = storage.get("City", city_id)

    if city is not None:
        if not request.is_json:
            abort(400, description='Not a JSON')

        request_body = request.get_json()

        if 'user_id' not in request_body:
            abort(400, description='Missing user_id')

        user = storage.get("User", request_body['user_id'])

        if user is None:
            abort(404)

        if 'name' not in request_body:
            abort(400, description='Missing name')

        request_body['city_id'] = city_id

        new_place = Place(**request_body)
        storage.new(new_place)
        storage.save()

        return make_response(new_place.to_dict(), 201)

    abort(404)


@app_views.route('/places/place_id>', methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    This method updates a Place object with the specified
    place_id
    """

    place = storage.get(Place, place_id)

    if place is not None:
        if not request.is_json:
            abort(400, description='Not a JSON')

        request_body = request.get_json()

        for key, value in request_body.items():
            if key not in ['id', 'user_id', 'city_id',
                           'created_at', 'updated_at']:
                setattr(place, key, value)

        place.save()

        return make_response(place.to_dict(), 200)
