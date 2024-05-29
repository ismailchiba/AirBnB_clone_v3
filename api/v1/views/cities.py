from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.city import City
from models.city import City
from models import storage
import json

@app_views.route("/cities/<city_id>/cities")
def get_cities(city_id):
    """ return cities of certain city """

    cities_dict = []
    for value in storage.all(City).values():
        if value.city_id == city_id:
            cities_dict.append(value.to_dict())
    if len(cities_dict) == 0:
        abort(404)
    return json.dumps(cities_dict, indent=2) + '\n'


@app_views.route("/cities/<city_id>")
def get_city(city_id):
    """ get city specific city"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return json.dumps(city.to_dict(), indent=2) + '\n'


@app_views.route("/cities/<city_id>", methods=['DELETE'])
def delete_city(city_id):
    """ delete city provided ID"""

    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return json.dumps({}, indent=2) + '\n'


@app_views.route("/cities/<city_id>/cities", methods=['POST'])
def create_city():
    """ create city object"""

    city_available = False
    obj_dict = request.get_json()
    if obj_dict is None:
        abort(400, "NOT a JSON")
    if "name" not in obj_dict.keys():
        abort(400, "Missing name")

    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    obj = City(**obj_dict)
    storage.new(obj)
    storage.save()
    x = obj.to_dict()
    return json.dumps(x, indent=2) + '\n', 201

@app_views.route("/cities/<city_id>", methods=["PUT"])
def city_update(city_id):
    """ update city """

    obj = storage.all(City)
    skip_keys = ["id", "state_id", "created_at", "updated_at"]
    available = False
    for key in obj.keys():
        if key.split('.')[-1] == city_id:
            available = True
            city = obj[key]
            obj_dict = city.to_dict()
            break

    if available is False:
        abort(404)
    up_dict = request.get_json()
    if up_dict is None:
        abort(400, "Not a JSON")
    storage.delete(city)
    storage.save()
    for ky, value in up_dict.items():
        if ky not in skip_keys:
            obj_dict[ky] = value
    obj = City(**obj_dict)
    storage.new(obj)
    storage.save()
    return json.dumps(obj.to_dict(), indent=2) + '\n', 200 

