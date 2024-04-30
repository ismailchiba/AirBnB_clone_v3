#!/usr/bin/python3
"""cities"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.city import City
from datetime import datetime
import uuid


@app_views.route('/cities/<cities_id>', methods=['GET'])
def get_city(city_id):
    """Retrieves a city object"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    return jsonify(city_obj[0])


@app_views.route('/cities/<city_id>', methods=["DELETE"])
def delete_city(city_id):
    """Deletes a City object"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_obj == []:
        abort(404)
    city_obj.remove(city_obj[0])
    for obj in all_cities:
        if obj.id == city_id:
            storage.delete(obj)
            storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>', methods=["PUT"])
def update_city(city_id):
    """updates a city"""
    all_cities = storage.all("City").values()
    city_obj = [obj.to_dict() for obj in all_cities if obj.id == city_id]
    if city_id == []:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    
    city_obj[0]['name'] = request.json['name']
    for obj in all_cities:
        if obj.id == city_id:
            obj.name = request.json['name']
     storage.save()
     return jsonify(states[0]), 200
