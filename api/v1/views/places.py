#!/usr/bin/python3
"""Places view module"""
from flask import jsonify, request, abort
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places_by_city(city_id):
    """Retrieve the list of all Place objects for a City"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """Retrieve a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """Delete a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({})


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, description="Missing name")
    place = Place(**data)
    place.city_id = city_id
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update a Place object"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()
    ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'])
def search_places():
    """Retrieves all Place objects based on the JSON in the request body"""
    if not request.json:
        return jsonify({"error": "Not a JSON"}), 400

    json_data = request.get_json()
    states = json_data.get('states', [])
    cities = json_data.get('cities', [])
    amenities = json_data.get('amenities', [])

    # Collect all place IDs from cities in states and cities directly
    place_ids = set()

    if states or cities:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        for place in city.places:
                            place_ids.add(place.id)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    for place in city.places:
                        place_ids.add(place.id)

    if amenities:
        # Filter places by amenities
        all_places = storage.all(Place)
        filtered_places = []
        for place in all_places.values():
            if all(amenity_id in [amenity.id for amenity in place.amenities]
                   for amenity_id in amenities):
                filtered_places.append(place)
        # Now intersect with place_ids to get the final result
        place_ids = set(place.id for place in filtered_places)
    else:
        # If amenities is empty, use the previously collected place_ids
        all_places = storage.all(Place)
        place_ids = set(place.id for place in all_places.values()
                        if place.id in place_ids)

    # Prepare response
    result = []
    for place_id in place_ids:
        place = storage.get(Place, place_id)
        if place:
            result.append(place.to_dict())

    return jsonify(result)
