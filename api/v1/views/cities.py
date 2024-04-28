#!/usr/bin/python3
""" Cities view /route mappings """

from api.v1.views import app_views
from flask import request
from flask import jsonify, abort, make_response
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_state_cities(state_id):
    """ returns cities of a state with id <state_id> """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    else:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def add_city(state_id):
    """ Adds city to state """
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    else:
        if request.is_json:
            kwargs_data = request.get_json()
            if kwargs_data.get('name') is not None:
                kwargs_data.update({"state_id": state_id})
                city = City(**kwargs_data)
                city.save()
                return make_response(jsonify(city.to_dict()), 201)
            abort(400, description="Missing name")
        abort(400, description="Not a JSON")


@app_views.route('/cities/<city_id>',
                 methods=['GET'], strict_slashes=False)
def get_cities(city_id):
    """ returns json of a city with city_id """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    else:
        return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_cities(city_id):
    """ deletes a city with id <city_id> """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    else:
        storage.delete(city)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>',
                 methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    """ updates a city with an id <city_id> """
    city = storage.get("City", city_id)
    if not city:
        abort(404)
    else:
        if request.is_json:
            kwargs_data = request.get_json()
            ignore = ['id', 'state_id', 'created_at', 'updated_at']
            for key, val in kwargs_data.items():
                if key not in ignore:
                    setattr(city, key, val)
            storage.save()
            return make_response(jsonify(city.to_dict()), 200)
        abort(400, description="Not a JSON")
