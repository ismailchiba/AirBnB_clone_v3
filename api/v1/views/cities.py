#!/usr/bin/python3

"""Interact with the City model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.city import City
from models.base_model import BaseModel as BM


cities = F(__name__)


@AV.route('/states/<state_id>/cities', methods=['GET', 'POST'])
def get_or_create_cities(state_id=None):
    """Get all cities / Create a new city w no Id"""
    sstate = storage.get('State', state_id)
    if sstate is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
        Citys = storage.all('City')
        response = [ccity.to_dict() for ccity in Citys.values()
                    if ccity.state_id == state_id]
        status = 200

    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') is None:
            abort(400, 'Missing name')
        RQ_json['state_id'] = state_id
        new_city = City(**RQ_json)
        new_city.save()
        response = new_city.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/cities/<city_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_city(city_id=None):
    """Get, delete or update a City object w a given identifier"""
    response = {}
    ccityy = storage.get('City', city_id)
    if ccityy is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = ccityy.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('name') == None:
            abort(400, 'Missing name')
         
        ccityy = City.db_update(RQ_json)
        ccityy.save()   # type: ignore
        response = ccityy.to_dict()   # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        ccityy.delete()   # type: ignore
        del ccityy
        status = 200
    return jsonify(response), status
