#!/usr/bin/python3

from flask import Blueprint, jsonify, abort, request, make_response
from werkzeug.exceptions import BadRequest
from models import storage
from models.state import State
from models.city import City

app_cities = Blueprint("app_cities", __name__)


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_cities.route("/<state_id>/cities", methods=['GET'])
def retrive_cities_by_state(state_id):
    """ This function return list of all cities related to a state
    """
    state = get_object_by_id(State, state_id)
    if not state:
        abort(404)
    return [city.to_dict() for city in state.cities]


@app_cities.route("/<city_id>", methods=['GET'])
def retrive_city(city_id):
    """ This function is used to retrive a specific city
        object using its id
    """
    city = get_object_by_id(City, city_id)
    if not city:
        abort(404)
    return city.to_dict()


@app_cities.route("/<city_id>", methods=['DELETE'])
def delete_state(city_id):
    """ This function is used to delete an city object when
        the DELETE method is called
    """
    city = get_object_by_id(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return {}, 200


@app_cities.route("/<state_id>/cities", methods=['POST'])
def create_city(state_id):
    """ This function creates a new city object
    """
    state = get_object_by_id(State, state_id)
    if state is None:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'name' not in request_data:
        abort(400, description="Missing name")
    new_city = City()
    new_city.name = request_data['name']
    new_city.state_id = state_id
    new_city.save()
    return new_city.to_dict(), 201


@app_cities.route("/<city_id>", methods=['PUT'])
def update_city(city_id):
    """ This function updates an existing city object
    """
    city = get_object_by_id(City, city_id)
    if not city:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at', 'state_id'):
            setattr(city, key, value)

    city.save()
    return city.to_dict(), 200
