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
    # Parse JSON data from request body
    search_data = request.get_json()

    # Validate JSON data
    if not search_data or not isinstance(search_data, dict):
        return jsonify({'error': 'Invalid JSON data'}), 400

    # Extract criteria from JSON data
    states = search_data.get('states', [])
    cities = search_data.get('cities', [])
    amenities = search_data.get('amenities', [])

    # Retrieve all Place objects if criteria are empty
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in places])

    # Implement search logic based on criteria (states, cities, amenities)
    # Your logic here...

    # Placeholder response for testing
    response = [{'name': 'Place 1'}, {'name': 'Place 2'}]
    return jsonify(response)
