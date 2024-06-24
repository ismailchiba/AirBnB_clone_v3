#!/usr/bin/python3
"""View for Place objs that handles all default RESTFul API actions"""

from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def all_places(city_id):
    """Retrieves list of all Place objects in given City"""
    data = []
    if storage.get(City, city_id) is None:
        abort(404)
    places = storage.all(Place).values()
    for place in places:
        if place.city_id == city_id:
            data.append(place.to_dict())
    return jsonify(data)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """Gets the Objs of a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(400)
    place = place.to_dict()
    return jsonify(place)


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def del_place(place_id):
    """Gets Place of an Obj"""
    emp_dict = {}
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify(emp_dict), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "name" not in data:
        abort(400, "Missing name")
    if storage.get(User, data["user_id"]) is None:
        abort(404)
    data['city_id'] = city_id
    place = Place(**data)
    place.save()
    place = place.to_dict()
    return jsonify(place), 201


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """Updates Place Objects"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if data is None:
        abort(400, "Not a JSON")
    for key, value in data.items():
        skeys = ["id", "user_id", "city_id", "created_at", "updated_at"]
        if key not in skeys:
            setattr(place, key, value)
    place.save()
    place = place.to_dict()
    return jsonify(place), 200
