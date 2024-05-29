#!/usr/bin/python3
"""Defines the view functions for managing cities in the API.

This module handles CRUD operations (Create, Read, Update, Delete) 
for city objects. It exposes endpoints for fetching all cities within 
a state, retrieving a specific city by ID, adding new cities to a 
state, and deleting or updating existing ones.

It utilizes the `storage` module for persistence and raises appropriate 
exceptions for invalid requests, resource not found errors, or missing 
required fields. Additionally, it considers cascading deletes for 
related models (Place and Review) when necessary (depending on the 
storage type).
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage, storage_t
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'])
@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_cities(state_id=None, city_id=None):
    """Dispatches incoming requests based on the HTTP method.

    This function acts as a central handler for all city-related 
    requests. It checks the request method and delegates the processing 
    to the appropriate function (get_cities, remove_city, etc.).
    """
    handlers = {
        'GET': get_cities,
        'DELETE': remove_city,
        'POST': add_city,
        'PUT': update_city,
    }
    if request.method in handlers:
        return handlers[request.method](state_id, city_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_cities(state_id=None, city_id=None):
    """Retrieves all cities within a state or a specific city by ID.

    If a state ID is provided, this function returns a list of all city 
    objects belonging to that state in JSON format. If a city ID is 
    provided, it fetches the corresponding city object and returns it 
    as JSON, raising a NotFound exception if the city or state is not found.
    """
    if state_id:
        state = storage.get(State, state_id)
        if state:
            cities = list(map(lambda x: x.to_dict(), state.cities))
            return jsonify(cities)
    elif city_id:
        city = storage.get(City, city_id)
        if city:
            return jsonify(city.to_dict())
    raise NotFound()


def remove_city(state_id=None, city_id=None):
    """Deletes a specific city and potentially related models.

    This function searches for the city with the provided ID and attempts 
    to remove it from storage. If the city is found, it is deleted. If 
    the storage type is not 'db' (implying a file-based system), it also 
    performs cascading deletes for associated Place and Review objects 
    to maintain data integrity. A success message is returned upon 
    successful deletion, otherwise a NotFound exception is raised.
    """
    if city_id:
        city = storage.get(City, city_id)
        if city:
            storage.delete(city)
            if storage_t != "db":
                for place in storage.all(Place).values():
                    if place.city_id == city_id:
                        for review in storage.all(Review).values():
                            if review.place_id == place.id:
                                storage.delete(review)
                        storage.delete(place)
            storage.save()
            return jsonify({}), 200
    raise NotFound()


def add_city(state_id=None, city_id=None):
    """Creates a new city object associated with a specific state.

    This function first verifies the existence of the state referenced 
    by the provided state ID. If the state is found, it expects a JSON 
    object containing the city data (including the 'name' property) in 
    the request body. It validates the request data and creates a new 
    City object if everything is correct. The new city is then associated 
    with the state and saved, returning the city data as JSON.

    Raises a NotFound exception if the state is not found or BadRequest 
    for invalid data or missing required fields.
    """
    state = storage.get(State, state_id)
    if not state:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return jsonify(city.to_dict()), 201


def update_city(state_id=None, city_id=None):
    """Updates an existing city object.

    This function retrieves the city with the provided ID and attempts 
    to update its properties based on the data sent in the request body 
    (JSON format). It validates the request data and ignores attempts to 
    update read-only properties ('id', 'state_id', 'created_at', 
    'updated_at'). A NotFound exception is raised if the city is not found.
    """
    xkeys = ('id', 'state_id', 'created_at', 'updated_at')
    if city_id:
        city = storage.get(City, city_id)
        if city:
            data = request.get_json()
            if type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict()), 200
    raise NotFound()
