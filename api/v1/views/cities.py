#!/usr/bin/python3
""" RESTFul Api - City """

from api.v1.views import app_views
from flask import Flask
from models import storage
from models.city import City
from models.state import State
from flask import jsonify, request, abort


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state_id(state_id):
    """ Retrieves the list of all City objects of a State """
    if request.method == 'GET':
        if storage.get(State, state_id) is not None:
            cities = []
            for ci in storage.all(City).values():
                if ci.state_id == state_id:
                    cities.append(ci.to_dict())
            return jsonify(cities)
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_city(city_id):
    """ Retrieves a City object. : GET /api/v1/cities/<city_id> """
    if request.method == 'GET':
        if storage.get(City, city_id) is not None:
            return jsonify(storage.get(City, city_id).to_dict())
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_city(city_id):
    """ Deletes a City object: DELETE /api/v1/cities/<city_id> """
    if request.method == 'DELETE':
        if storage.get(City, city_id) is not None:
            storage.delete(storage.get(City, city_id))
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_new_city(state_id):
    """ Creates a City: POST /api/v1/states/<state_id>/cities """
    if request.method == 'POST':
        if storage.get(State, state_id) is not None:
            req_type = request.headers.get('Content-Type')
            if req_type != 'application/json':
                return jsonify('Not a JSON'), 400
            dict_req_name = request.get_json()
            if 'name' not in dict_req_name:
                return jsonify('Missing name'), 400
            new_obj_City = City(**dict_req_name)
            new_obj_City.state_id = state_id
            new_obj_City.save()
            return jsonify(new_obj_City.to_dict()), 201
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object: PUT /api/v1/cities/<city_id> """
    if request.method == 'PUT':
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req = request.get_json()
        if storage.get(City, city_id) is not None:
            if 'name' in dict_req:
                storage.get(City, city_id).name = dict_req['name']
                storage.get(City, city_id).save()
                return jsonify(storage.get(City, city_id).to_dict()), 200
        abort(404)
