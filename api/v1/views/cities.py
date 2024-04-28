#!/usr/bin/python3
"""
    Cities view for the API.
"""
from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def cities_by_state(state_id):
    """Retrieves the list of all cities of a State objects"""
    objs = storage.get(State, state_id)
    if not objs:
        abort(404)
    return jsonify([city.to_dict() for city in objs.cities])


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def cities(city_id):
    """Retrieve a city from cities using id"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_city(city_id):
    """Deletes a City object"""
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def add_city():
    """Returns the new city and returns 201"""
    obj_state = storage.get(State, state_id)
    if not obj_state:
        abort(404)

    try:
        new_obj = request.get_json()
    except Exception:
        abort(400, "Not a JSON")
    if 'name' not in new_obj:
        abort(400, "Missing name")
    obj = City(**new_obj)
    setattr(obj, 'state_id', state_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """ Updates a City object """
    obj = storage.get(City, city_id)
    if not obj:
        abort(404)

    try:
        req = request.get_json()
    except Exception:
        abort(400, "Not a JSON")

    for key, value in req.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(obj, key, value)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
