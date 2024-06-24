#!/usr/bin/python3
"""
create a new view for City objects that handles all default RESTful API
actions
"""
from models import storage
from api.v1.views import app_views
from flask import make_response, jsonify, abort, request
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_cities(state_id, cities=None):
    """list of all City objects of a State"""
    state_inst = storage.get('State', state_id)
    if not state_inst:
        abort(404)

    if request.method == 'GET':
        city_instances = [city.to_dict() for city in state_inst.cities]
        return make_response(jsonify(city_instances), 200)

    elif request.method == 'POST':
        if not request.is_json or not request.get_json().get('name', None):
            abort(400)
        data = request.get_json()
        data['state_id'] = state_id
        new_inst = City(**data)
        new_inst.save()
        data = storage.get(City, new_inst.id).to_dict()
        return make_response(jsonify(data), 201)

    elif request.method == 'HEAD':
        return make_response(jsonify(""), 200)


@app_views.route('/cities/<city_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def city_obj(city_id):
    """Retrieves a City Object"""
    city_inst = storage.get(City, city_id)
    if not city_inst:
        abort(404)

    if request.method == 'GET':
        return make_response(jsonify(city_inst.to_dict()), 200)

    elif request.method == 'DELETE':
        storage.delete(city_inst)
        storage.save()
        return jsonify({}), 200

    elif request.method == 'PUT':
        if not request.is_json:
            abort(400)
        data = request.get_json()
        for key in data.keys():
            if key not in ['id', 'state_id', 'created_at', 'updated_at']:
                setattr(city_inst, key, data[key])
        city_inst.save()
        return make_response(jsonify(city_inst.to_dict()), 200)

    elif request.method == 'HEAD':
        return make_response(jsonify(""), 200)
