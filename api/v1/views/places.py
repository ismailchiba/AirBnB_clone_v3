#!/usr/bin/python3

"""Interact with the Place model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.place import Place
from models.base_model import BaseModel as BM


places = F(__name__)


@AV.route('/cities/<city_id>/places', methods=['GET', 'POST'])
def get_or_create_places(city_id=None):
    """Get all places / Create a new place w no Id"""
    City = storage.get('City', city_id)
    if City is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
        cities = storage.all('City')
        response = [place.to_dict() for place in cities.values()
                    if place.city_id == city_id]
        status = 200

    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') is None:
            abort(400, 'Missing name')
        user_Id = RQ_json.get('user_id')
        if user_Id is None:
            abort(400, 'Missing user_id')
        if storage.get('User', user_Id) is None:
            abort(404, 'Not found')

        new_user = Place(**RQ_json)
        new_user.save()
        response = new_user.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/places/<place_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_place(place_id=None):
    """Get, delete or update a Place object w a given identifier"""
    response = {}
    place = storage.get('Place', place_id)
    if place is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = place.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') is None:
            abort(400, 'Missing name')
        user_Id = RQ_json.get('user_id')
        if user_Id is None:
            abort(400, 'Missing user_id')
        if storage.get('User', user_Id) is None:
            abort(404, 'Not found')

        place = Place.db_update(RQ_json)
        place.save()   # type: ignore
        response = place.to_dict()   # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        place.delete()   # type: ignore
        del place
        status = 200
    return jsonify(response), status
