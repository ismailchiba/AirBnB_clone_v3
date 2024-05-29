from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.city import City
from models.state import State
from models import storage
import json


@app_views.route("/states/<state_id>/cities")
@app_views.route("/states/<state_id>/cities/")
def get_cities(state_id):
    """ return cities from a given state<state_id> """

    cities_dict = []
    valid_state = False
    for state in storage.all(State).values():
        if state.id == state_id:
            valid_state = True
            break
    if valid_state is False:
        abort(404)

    for city in storage.all(City).values():
        if city.state_id == state_id:
            cities_dict.append(city.to_dict())

    return jsonify(cities_dict), 200


@app_views.route("/cities/<city_id>")
@app_views.route("/cities/<city_id>/")
def get_city(city_id):
    """ retrieve city"""

    for city in storage.all(City).values():
        if city.id == city_id:
            return jsonify(city.to_dict()), 200

    abort(404)


@app_views.route("/cities/<city_id>", methods=['DELETE'])
@app_views.route("/cities/<city_id>/", methods=['DELETE'])
def delete_city(city_id):
    """ delete city object"""

    for city in storage.all(City).values():
        if city.id == city_id:
            storage.delete(City)
            storage.save()
            return jsonify(city.to_dict()), 200

    abort(404)


@app_views.route("/states/<state_id>/cities", methods=['POST'])
@app_views.route("/states/<state_id>/cities/", methods=['POST'])
def create_city(state_id):
    """ create city object belonging to a state"""

    valid_state = False
    for state in storage.all(State).values():
        if state.id == state_id:
            valid_state = True
            break
    if valid_state is False:
        abort(404)

    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, "NOT a JSON")
    if "name" not in obj_dict.keys():
        abort(400, "Missing name")

    obj_dict["state_id"] = state_id

    new_city = City(**obj_dict)
    storage.new(new_city)
    storage.save()
    city_dict = new_city.to_dict()
    return jsonify(city_dict), 201


@app_views.route("/cities/<city_id>", methods=["PUT"])
@app_views.route("/cities/<city_id>/", methods=["PUT"])
def city_update(city_id):
    """ update city """

    skip_keys = ["id", "state_id", "created_at", "updated_at"]
    for city in storage.all(City).values():
        if city.id == city_id:
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            city_dict = city.to_dict()
            storage.delete(city)
            storage.save()

            for key, value in update_info.items():
                if key not in skip_keys:
                    city_dict[key] = value
            updated_city = City(**city_dict)
            storage.new(updated_city)
            storage.save()
            return jsonify(city_dict), 200

    abort(404)
