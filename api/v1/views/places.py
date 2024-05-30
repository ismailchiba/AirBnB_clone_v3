#!/usr/bin/python3
"""Module for the new view of Place objects"""

from api.v1.views import app_views
from models import storage
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import abort, request, jsonify


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["GET"])
def get_places(city_id):
    """Retrieves places based on city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = city.places
    places.ls = []
    for place in places:
        places_ls.append(place.to_dict())
    return jsonify(places_list), 200


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["GET"])
def get_place(place_id):
    """Retrieves a place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict()), 200


@app_views.route("/places/<place_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_place(place_id):
    """deletes place object by id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", strict_slashes=False,
                 methods=["POST"])
def create_place(city_id):
    """create a new place based on the city id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    user_id = data.get('user_id')
    if not user_id:
        abort(400, "Missing user_id")
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if "name" not in data:
        abort(400, "Missing name")
    new_place = Place(city_id=city.id, **data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", strict_slashes=False, methods=["PUT"])
def update_place(place_id):
    """update place by place id"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            seattr(place, k, v)
    storage.save()
    return jsonify(place.to_dict()), 200


"""
@app_views.route("/places_search", strict_slashes=False,
                 methods=["POST"])
def search_places():

        Retrieves all Place objects
        depending of the JSON in the body of the request.

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for p in list_places:
        d = p.to_dict()
        d.pop('amenities', None)
        places.append(d)

    return jsonify(places)
"""
