#!/usr/bin/python3
"""
This module handles all default RESTFul API actions:
    - Retrieves a list of all Place objects of a city
    - Retrieves a Place object
    - Creates a Place object
    - Updates a Place object
    - Deletes a Place object
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Retrieves a list of all place objects of a city"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    places = [obj.to_dict() for obj in city.places]

    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Retrieves a place object"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place object"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place object"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    data['city_id'] = city_id

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)

    place = Place(**data)
    place.save()

    return jsonify(place.to_dict()), 201


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place object"""

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at', 'user_id', 'city_id']:
            setattr(place, k, v)
    place.save()

    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def search_all_places():
    """
    Retrieves all Place objects depending
    on the JSON in the body of the request
    """
    data = request.get_json()

    if not data:
        return jsonify({"error": "Not a JSON"}), 400

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    # Retrieve places based on states and cities
    places = []
    if states or cities:
        for state_id in states:
            state = storage.get(State, state_id)
            if state:
                for city in state.cities:
                    if city.id not in cities:
                        cities.append(city.id)
        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    # Filter places based on amenities
    if amenities:
        filtered_places = []
        for place in places:
            has_all_amenities = True
            for amenity_id in amenities:
                amenity_found = False
                for amenity in place.amenities:
                    if amenity.id == amenity_id:
                        amenity_found = True
                        break
                if not amenity_found:
                    has_all_amenities = False
                    break
            if has_all_amenities:
                filtered_places.append(place)
        places = filtered_places

    return jsonify([place.to_dict() for place in places])
