#!/usr/bin/python3
"""Place objects that handles all default RESTFul API actions."""

from models import storage
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.city import City
from models.user import User
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>/', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """
    Retrieves a specific Place object based on id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object based on id provided
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Creates a Place
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    if 'user_id' not in data:
        abort(400, "Missing user_id")
    user_id = data.get('user_id')
    if not storage.get(User, user_id):
        abort(404)
    if 'name' not in data:
        abort(400, "Missing name")

    instance = Place(**data)
    instance.city_id = city.id
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """
    Updates a Place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore:
            setattr(place, key, value)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """Search for places based on JSON request"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    place_ids = set()
    for state_id in states:
        state = storage.get(State, state_id)
        if state:
            for city in state.cities:
                place_ids.update({place.id for place in city.places})

    for city_id in cities:
        city = storage.get(City, city_id)
        if city:
            place_ids.update({place.id for place in city.places})

    if amenities:
        amenity_ids = set(amenities)
        for place_id in place_ids.copy():
            place = storage.get(Place, place_id)
            if place and not (
                    amenity_ids <= set(amen.id for amen in place.amenities)):
                place_ids.remove(place_id)

    places = [storage.get(Place, place_id) for place_id in place_ids]
    return jsonify([place.to_dict() for place in places if place])
