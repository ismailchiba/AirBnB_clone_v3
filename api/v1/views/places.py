#!/usr/bin/python3
"""
Defines API routes for handling Place objects
"""
from flask import abort, jsonify, request
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'], strict_slashes=False)
def get_places_by_city(city_id):
    """
    Retrieves the list of all Place objects of a City: GET /api/v1/cities/<city_id>/places
    If the city_id is not linked to any City object, raise a 404 error
    """
    city = storage.get(City, city_id)
    if not city:
         abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_places(place_id):
    """
    Retrieves a Place object. : GET /api/v1/places/<place_id>
    If the place_id is not linked to any Place object, raise a 404 error
    """
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'], strict_slashes=False)
def delete_place(place_id):
    """
    Deletes a Place object: DELETE /api/v1/places/<place_id>
    If the place_id is not linked to any Place object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'], strict_slashes=False)
def create_place(city_id):
    """
    Creates a Place: POST /api/v1/cities/<city_id>/places
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the city_id is not linked to any City object, raise a 404 error
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object, raise a 404 error
    If the dictionary doesn’t contain the key name, raise a 400 error with the message Missing name
    Returns the new Place with the status code 201
    """
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'name' not in data:
        abort(400, 'Missing name')
    
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """
    Updates a Place object: PUT /api/v1/places/<place_id>
    If the place_id is not linked to any Place object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the Place object with all key-value pairs of the dictionary
    Ignore keys: id, user_id, city_id, created_at and updated_at
    Returns the Place object with the status code 200
    """
    place = storage.get(Place, place_id)
    if place:
        if not request.get_json():
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(place, key, value)

        place.save()
        return jsonify(place.to_dict()), 200
    else:
        abort(404)


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def search_places():
    """
    Search for places based on JSON data in request body
    """
    if not request.get_json():
        abort(400, 'Not a JSON')

    data = request.get_json()
    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities = data.get('amenities', [])

    places = []
    if not states and not cities and not amenities:
        places = storage.all(Place).values()
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        if city not in cities:
                            cities.append(city)

        for city_id in cities:
            city = storage.get(City, city_id)
            if city:
                places.extend(city.places)

    if amenities:
        amenities_set = set(amenities)
        places = [place for place in places if amenities_set.issubset(set(place.amenity_ids))]

    return jsonify([place.to_dict() for place in places])
