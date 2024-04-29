#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User


@app_views.route("cities/<city_id>/places", methods=['GET', 'POST'])
def places_without_id(city_id):
    """Create a new place or return all the places"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        places_list = [place.to_dict() for place in city.places]
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
        json['city_id'] = city_id
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


@app_views.route("/places_search", methods=['POST'])
def search_places():
    """Search for places based on the request body"""
    json = request.get_json()
    if json is None:
        abort(400, "Not a JSON")

    states_ids = json.get('states', [])
    cities_ids = json.get('cities', [])
    amenities_ids = json.get('amenities', [])

    if (json == {} or
            (states_ids == [] and cities_ids == [] and amenities_ids == [])):
        places = storage.all(Place).values()

    cities = set()

    for state_id in states_ids:
        state = storage.get(State, state_id)
        if state is None:
            continue
        if state.cities:
            cities = cities.union(set(state.cities))

    for city_id in cities_ids:
        city = storage.get(City, city_id)
        if city:
            cities.add(city)

    places = []
    for city in cities:
        places += city.places

    amenities = []
    for amenity_id in amenities_ids:
        amenity = storage.get(Amenity, amenity_id)
        if amenity:
            amenities.append(amenity)

    if amenities:
        for place in places[:]:
            for amenity in amenities:
                if amenity not in place.amenities:
                    places.remove(place)
                    break

    places = [place.to_dict() for place in places]
    return jsonify(places)
