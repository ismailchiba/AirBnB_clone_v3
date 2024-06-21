#!/usr/bin/python3
"""
Place rest API
"""
from flask import request
from flask import abort
from flask import jsonify
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from api.v1.views import app_views


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['GET'])
def get_place_byCityId(city_id):
    """get that place with this city id"""
    city = storage.get(City, city_id)
    if city is None:
        return (abort(404))
    places = [p.to_dict() for p in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['GET'])
def get_place_byItsId(place_id):
    """retreive place by its id"""
    place = storage.get(Place, place_id)
    if not place:
        return (abort(404))
    return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places',
                 strict_slashes=False, methods=['POST'])
def createaAPlace(city_id):
    """Create a place for a given city id"""
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    city = storage.get(City, city_id)
    if not city:
        return (abort(404))
    if not data:
        return (abort(400, 'Not a JSON'))
    if 'user_id' not in data.keys():
        return (abort(400, 'Missing user_id'))
    if 'name' not in data.keys():
        return (abort(400, 'Missing name'))
    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        return (abort(404))
    place = Place(city_id=city_id, **data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['PUT'])
def updatePlace(place_id):
    """update place"""
    place = storage.get(Place, place_id)
    if place is None:
        return (abort(404))
    try:
        data = request.get_json()
    except:
        return (abort(400, 'Not a JSON'))
    if not data:
        return (abort(400, 'Not a JSON'))
    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(place, k, v)
    place.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>',
                 strict_slashes=False, methods=['DELETE'])
def delete_place(place_id):
    """delete that place"""
    place = storage.get(Place, place_id)
    if place is None:
        return (abort(404))
    storage.delete(place)
    storage.save()
    return jsonify({}), 200
