#!/usr/bin/python3
"""This creates a view for place"""

from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
import requests
import json
from os import getenv


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_by_city(city_id):
    """This retrieves a list of all Place objects"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """This retrieves a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """This deletes a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """This creates a place object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get("User", data["user_id"])
    if not user:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    place = Place(**data)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """This updates a place object by Id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, 'Not a JSON')

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """This retrieves all place objects depending on the request"""
    body = request.get_json()
    if body is None:
        abort(400, 'Not a JSON')
    if not body or (
        not body.get("states")
        and not body.get("cities")
        and not body.get("amenities")
    ):
        places = storage.all(Place)
        return jsonify([place.to_dict() for place in places.values()])

    places = []

    if body.get("states"):
        states = [storage.get("State", id) for id in body.get("states")]

        for state in states:
            for city in state.cities:
                for place in city.places:
                    places.append(place)

    if body.get("cities"):
        cities = [storage.get("City", id) for id in body.get("cities")]

        for city in cities:
            for place in city.places:
                if place not in places:
                    places.append(place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    if body.get("amenities"):
        amenities = [storage.get("Amenity", id) for id in
                     body.get("amenities")]
        count = 0
        limit = count(places)
        HBNB_API_HOST = getenv("HBNB_API_HOST")
        HBNB_API_PORT = getenv("HBNB_API_PORT")

        port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
        f_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
        while count < limit:
            place = places[count]
            url = f_url + "{}/amenities"
            requ = url.format(place.id)
            response = requests.get(requ)
            ame_d = json.loads(response.text)
            ame = [storage.get("Amenity", o["id"]) for o in ame_d]
            for amenity in amenities:
                if amenity not in amenities:
                    places.pop(count)
                    count -= 1
                    limit -= 1
                    break
            count += 1
    return jsonify([place.to_dict() for place in places])
