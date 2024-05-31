#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.place import Place
from models.city import City
from models.user import User
from models import storage


""" places objects view methods, GET/POST/PUT/DELETE request methods"""


@app_views.route("/cities/<city_id>/places")
@app_views.route("/cities/<city_id>/places/")
def get_places(city_id):
    """ return places from a given <city_id> """

    valid_city = False
    for city in storage.all(City).values():
        if city.id == city_id:
            valid_city = True
            break
    if valid_city is False:
        abort(404)

    places_list = []
    for place in storage.all(Place).values():
        if place.city_id == city_id:
            places_list.append(place.to_dict())

    return jsonify(places_list), 200


@app_views.route("/places/<place_id>")
@app_views.route("/places/<place_id>/")
def get_place(place_id):
    """ retrieve place"""

    for place in storage.all(Place).values():
        if place.id == place_id:
            return jsonify(place.to_dict()), 200

    abort(404)


@app_views.route("/places/<place_id>", methods=['DELETE'])
@app_views.route("/places/<place_id>/", methods=['DELETE'])
def delete_place(place_id):
    """ delete place object"""

    for place in storage.all(Place).values():
        if place.id == place_id:
            storage.delete(place)
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route("/cities/<city_id>/places", methods=['POST'])
@app_views.route("/cities/<city_id>/places/", methods=['POST'])
def create_place(city_id):
    """ create place object belonging to a <city_id>"""

    valid_city = False
    for city in storage.all(City).values():
        if city.id == city_id:
            valid_city = True
            break
    if valid_city is False:
        print("invalid city")
        abort(404)

    place = request.get_json()
    if place is None:
        abort(400, "NOT a JSON")
    if "user_id" not in place.keys():
        abort(400, "Missing user_id")
    valid_user = False
    for user in storage.all(User).values():
        if user.id == place["user_id"]:
            valid_user = True
    if valid_user is False:
        print("invalid user")
        abort(400)
    if "name" not in place.keys():
        abort(400, "Missing name")

    place["city_id"] = city_id

    new_place = Place(**place)
    storage.new(new_place)
    storage.save()
    return jsonify(place), 201


@app_views.route("/places/<place_id>", methods=["PUT"])
@app_views.route("/places/<place_id>/", methods=["PUT"])
def place_update(place_id):
    """ update place """

    skip_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for place in storage.all(Place).values():
        if place.id == place_id:
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            place_dict = place.to_dict()
            storage.delete(place)
            storage.save()

            for key, value in update_info.items():
                if key not in skip_keys:
                    place_dict[key] = value
            updated_place = Place(**place_dict)
            storage.new(updated_place)
            storage.save()
            return jsonify(place_dict), 200

    abort(404)
