#!/usr/bin/python3
"""
    Handles all default RESTful API actions for Place objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("/cities/<city_id>/places", strict_slashes=False)
def get_places(city_id):
    """
        Retrieves the list of all Place objects of a City
    """
    all_places = storage.all(Place)
    place_list = list()
    for place in all_places.values():
        if city_id == place.city_id:
            place_list.append(place.to_dict())
    if place_list:
        return Response(json.dumps(place_list, indent=2),
                        mimetype="application/json", status=200)
    abort(404)


@app_views.route("/places/<place_id>", strict_slashes=False)
def get_place(place_id):
    """
        Retrieves a Place object
    """
    all_places = storage.all(Place)
    for place in all_places.values():
        if place_id == place.id:
            return Response(json.dumps(place.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)


@app_views.route("places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
        Deletes a Place object
    """
    all_places = storage.all(Place)
    keep_place = None
    for key, val in all_places.items():
        if place_id == val.id:
            keep_place = key
            break
    if keep_place:
        storage.delete(all_places[keep_place])
        storage.save()
        return Response(json.dumps({}, indent=2),
                        mimetype="application/json", status=200)
    abort(404)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def post_place(city_id):
    """
        Creates a Place object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    if not data.get("user_id"):
        return "Missing user_id", 400
    if not data.get("name"):
        return "Missing name", 400
    user_id = data.get("user_id")
    keep_user = None
    all_users = storage.all(User)
    for user in all_users.values():
        if user_id == user.id:
            keep_user = user
            break
    if not keep_user:
        abort(404)
    else:
        all_cities = storage.all(City)
        for city in all_cities.values():
            if city_id == city.id:
                instance = Place()
                for key, val in data.items():
                    setattr(instance, key, val)
                instance.city_id = city_id
                instance.user_id = user_id
                instance.save()
                return Response(json.dumps(instance.to_dict(), indent=2),
                                mimetype="application/json", status=201)
        abort(404)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def put_place(place_id):
    """
        Update a Place object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    all_places = storage.all(Place)
    for place in all_places.values():
        if place_id == place.id:
            for key, val in data.items():
                if key == "id" or key == "user_id" or \
                   key == "city_id" or key == "created_at" or \
                   key == "updated_at":
                    continue
                setattr(place, key, val)
            storage.save()
            return Response(json.dumps(place.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)
