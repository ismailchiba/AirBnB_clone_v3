#!/usr/bin/python3
""" RESTFul Api - City """

from api.v1.views import app_views
from flask import Flask
from models import storage
from models.city import City
from models.user import User
from models.place import Place
from flask import jsonify, request, abort


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def places_by_city_id(city_id):
    """ Retrieves the list of all Place objects of a City """
    if request.method == 'GET':
        if storage.get(City, city_id) is not None:
            places = []
            for pl in storage.all(Place).values():
                if pl.city_id == city_id:
                    places.append(pl.to_dict())
            return jsonify(places)
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def retrieve_one_place(place_id):
    """ Retrieves a Place object. : GET /api/v1/places/<place_id> """
    if request.method == 'GET':
        if storage.get(Place, place_id) is not None:
            return jsonify(storage.get(Place, place_id).to_dict())
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_one_place(place_id):
    """ Deletes a Place object: DELETE /api/v1/places/<place_id> """
    if request.method == 'DELETE':
        if storage.get(Place, place_id) is not None:
            storage.delete(storage.get(Place, place_id))
            storage.save()
            return jsonify({}), 200
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_new_place(city_id):
    """ Creates a Place: POST /api/v1/cities/<city_id>/places """
    if request.method == 'POST':
        if storage.get(City, city_id) is not None:
            req_type = request.headers.get('Content-Type')
            if req_type != 'application/json':
                return jsonify('Not a JSON'), 400
            dict_req = request.get_json()
            if 'user_id' not in dict_req:
                return jsonify('Missing user_id'), 400
            if storage.get(User, dict_req['user_id']) is None:
                abort(404)
            else:
                if 'name' not in dict_req:
                    return jsonify('Missing name'), 400
                new_obj_Place = Place(**dict_req)
                new_obj_Place.city_id = city_id
                new_obj_Place.user_id = dict_req['user_id']
                new_obj_Place.save()
                return jsonify(new_obj_Place.to_dict()), 201
        abort(404)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ Updates a Place object: PUT /api/v1/places/<place_id> """
    if request.method == 'PUT':
        place = storage.get(Place, place_id)
        req_type = request.headers.get('Content-Type')
        if req_type != 'application/json':
            return jsonify('Not a JSON'), 400
        dict_req = request.get_json()
        if place is not None:
            if 'name' in dict_req:
                place.name = dict_req['name']
            if 'description' in dict_req:
                place.description = dict_req['description']
            if 'number_rooms' in dict_req:
                place.number_rooms = dict_req['number_rooms']
            if 'number_bathrooms' in dict_req:
                place.number_bathrooms = dict_req['number_bathrooms']
            if 'max_guest' in dict_req:
                place.max_guest = dict_req['max_guest']
            if 'price_by_night' in dict_req:
                place.price_by_night = dict_req['price_by_night']
            if 'latitude' in dict_req:
                place.latitude = dict_req['latitude']
            if 'longitude' in dict_req:
                place.longitude = dict_req['longitude']
            storage.save()
            return jsonify(place.to_dict()), 200
        abort(404)
