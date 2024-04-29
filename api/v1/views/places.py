#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.user import User


@app_views.route("cities/<city_id>/places", methods=['GET', 'POST'])
def places_without_id(city_id):
    """Create a new place or return all the places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places_list = []
        places_dict = city.places
        for place in places_dict.values():
            places_list.append(place.to_dict())
        return jsonify(places_list)

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        user_id = json.get('user_id')
        if user_id is None:
            abort(400, "Missing user_id")
        if json.get('name') is None:
            abort(400, "Missing name")
        if storage.get(User, user_id) is None:
            abort(404)
        place = Place(**json)
        place.save()
        return jsonify(place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['GET', 'PUT', 'DELETE'])
def places_with_id(place_id=None):
    """Perform READ UPDATE DELETE operations on a place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(place.to_dict())

    if request.method == 'DELETE':
        place.delete()
        del place
        return jsonify({})

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        place.update(**json)
        return jsonify(place.to_dict())
