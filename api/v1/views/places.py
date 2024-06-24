#!/usr/bin/python3
"""A new view for State objects
that handles all default RESTFul API actions"""
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route("/cities/<city_id>/places",
                 methods=["GET"], strict_slashes=False)
def place_city(city_id):
    """Retrieve place by a city ID"""
    obj_city = storage.get(City, city_id)
    if obj_city is None:
        abort(404)
    place_in_city = []
    for p_city in obj_city.places:
        place_in_city.append(p_city.to_dict())
    return jsonify(place_in_city)


@app_views.route("/places/<place_id>",
                 methods=["GET"], strict_slashes=False)
def place_id(place_id):
    """Retrieve a place by ID"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)
    return jsonify(obj_place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """Delete a place by ID"""
    obj_place = storage.get(Place, place_id)
    if obj_place is None:
        abort(404)

    storage.delete(obj_place)
    storage.save()

    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_post(city_id):
    """Create a new place in city ID"""
    city_obj = storage.get(City, city_id)
    if not city_obj:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in data:
        return jsonify({"error": 'Missing text'}), 400
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    name = data['name']
    user_id = data['user_id']

    user_data = storage.get(User, user_id)

    if not user_data:
        abort(404)

    new_place = Place(name=name, user_id=user_id, city_id=city_id)
    new_place.save()

    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_put(place_id):
    """Update a place by ID"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    data = request.get_json()
    if data is None:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in data.items():
        if key not in ['id', 'user_id', 'created_at', 'updated_at']:
            setattr(obj_place, key, value)

    obj_place.save()

    return jsonify(obj_place.to_dict()), 200
