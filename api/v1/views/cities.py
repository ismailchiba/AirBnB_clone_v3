#!/usr/bin/python3
"""
    Handles all default RESTFul API actions for City objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models import storage
from models.city import City
from models.state import State


@app_views.route("/states/<state_id>/cities", strict_slashes=False)
def get_cities(state_id):
    """
        show all cities in a state
    """
    all_cities = storage.all(City)
    city_list = list()
    if all_cities:
        for val in all_cities.values():
            if state_id == val.state_id:
                city_dict = val.to_dict()
                city_list.append(city_dict)
    if city_list:
        city_json = json.dumps(city_list, indent=2)
        return Response(city_json, mimetype="application/json", status=200)
    abort(404)


@app_views.route("/cities/<city_id>", strict_slashes=False)
def get_city(city_id):
    """
        Retrieve a City object
    """
    all_cities = storage.all(City)
    keep_city = None
    if all_cities:
        for val in all_cities.values():
            if city_id == val.id:
                city_dict = val.to_dict()
                keep_city = val
                break
    if keep_city:
        city_json = json.dumps(city_dict, indent=2)
        return Response(city_json, mimetype="application/json", status=200)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["DELETE"])
def delete_city(city_id):
    """
        Deletes a City object
    """
    all_cities = storage.all(City)
    keep_city = None
    for key, val in all_cities.items():
        if city_id == val.id:
            keep_city = key
            break
    if keep_city:
        storage.delete(all_cities[keep_city])
        storage.save()
        city_json = json.dumps({}, indent=2)
        return Response(city_json, mimetype="application/json", status=200)
    abort(404)


@app_views.route("/states/<state_id>/cities", methods=["POST"],
                 strict_slashes=False)
def post_city(state_id):
    """
        Creates a City object
    """
    data = request.get_json()
    if not data:
        return Response("Not a JSON", status=400)
    name = data.get("name")
    if not name:
        return "Missing name", 400
    all_states = storage.all(State)
    for val in all_states.values():
        if state_id == val.id:
            instance = City()
            instance.state_id = state_id
            for key, value in data.items():
                setattr(instance, key, value)
            instance.save()
            instance_dict = instance.to_dict()
            instance_json = json.dumps(instance_dict, indent=2)
            return Response(instance_json, mimetype="application/json",
                            status=201)
    abort(404)


@app_views.route("/cities/<city_id>", methods=["PUT"],
                 strict_slashes=False)
def put_city(city_id):
    """
        Updates a City object
    """
    keep_city = None
    data = request.get_json()
    if not data:
        return "Not a JSON", 400
    all_cities = storage.all(City)
    for val in all_cities.values():
        if city_id == val.id:
            keep_city = val
            break
    if keep_city:
        for key, value in data.items():
            if key == "id" or key == "state_id" or \
               key == "created_at" or key == "updated_at":
                continue
            setattr(val, key, value)
        val.save()
        val_dict = val.to_dict()
        val_json = json.dumps(val_dict, indent=2)
        return Response(val_json, mimetype="application/json", status=200)
    abort(404)
