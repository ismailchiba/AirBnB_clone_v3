#!/usr/bin/python3

from models.city import City
from flask import jsonify, request, abort, make_response
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    for city in state.cities:
        city_list = city.to_dict()
    return jsonify(city_list)


@ app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def one_city(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    city = city_obj.to_dict()
    return jsonify(city)


@ app_views.route('/cities/<city_id>',
    methods = ['DELETE'],
     strict_slashes = False)
def del_city(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    storage.delete(city_obj)
    storage.save()
    return jsonify({}), 200

@ app_views.route('/states/<state_id>/cities',
                  methods = ['POST'], strict_slashes = False)
def create_post_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    if 'name' not in data:
        return make_response(jsonify({"error": "Missing name"}), 400)

    new_city = City(name=data['name'], state_id=state_id)
    new_city.save()
    return jsonify(new_city.to_dict()), 201

@ app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)

    data = request.get_json(silent=True)
    if not data:
        return make_response(jsonify({"error": "Not a JSON"})), 400

    for key, value in data.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city_obj, key, value)
    city_obj.save()
    return jsonify(city_obj.to_dict())
