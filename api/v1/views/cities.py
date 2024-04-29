#!/usr/bin/python3
"""return JSON """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/cities', methods=['GET'], strict_slashes=False)
def get_cities():
    city_api = []
    cities = storage.all(State).values()
    for city in cities:
        city_api.append(city.to_dict())
    return jsonify(city_api)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city_by_id(city_id):
    city = storage.get(State, city_id)
    if city:
        city_api = city.to_dict()
        return jsonify(city_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city_by_id(city_id):
    city = storage.get(State, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def post_city_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city_by_id(city_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    city = storage.get(State, city_id)
    if city:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(city, k, v)
                storage.save()
        return jsonify(city.to_dict()), 201
    else:
        abort(404)
