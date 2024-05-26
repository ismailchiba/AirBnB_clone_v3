#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for Place objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User

api_route_1 = "/cities/<string:city_id>/places"
api_route_2 = "/places/<string:place_id>"


@app_views.route(api_route_1, methods=["GET"], strict_slashes=False)
def get_city_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """

    city = storage.get(City, city_id)

    if city is None:
        abort(404)

    places_list = []

    for place in city.places:
        places_list.append(place.to_dict())

    response = jsonify(places_list), 200

    return response


@app_views.route(api_route_1, methods=["POST"], strict_slashes=False)
def create_place(city_id):
    """
    Create a new place.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new place and the HTTP status code 201.
    """
    city = storage.get(City, city_id)

    if not city:
        abort(404)

    body = request.get_json(silent=True)
    place_fields = ["user_id", "name"]

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for field in place_fields:
        if field not in body:
            message = "Missing {}".format(field)
            return make_response(jsonify({"error": message}), 400)

    body["city_id"] = city_id
    user = storage.get(User, body["user_id"])

    if not user:
        abort(404)

    new_place = Place(**body)

    new_place.save()

    response = jsonify(new_place.to_dict()), 201

    return make_response(response)


@app_views.route(api_route_2, methods=["GET"], strict_slashes=False)
def get_place_by_id(place_id):
    """
    Retrieves a Place object
    """

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    response = jsonify(place.to_dict()), 200

    return response


@app_views.route(api_route_2, methods=["DELETE"], strict_slashes=False)
def delete_place(place_id):
    """
    Delete a place by its ID.

    Args:
        place_id (str): The ID of the place to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    storage.delete(place)
    storage.save()

    return jsonify({})


@app_views.route(api_route_2, methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Update a place by its ID.

    Args:
        place_id (str): The ID of the place to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated place and the HTTP status code 200.

    Raises:
        404: If the place with the specified ID does not exist.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    place = storage.get(Place, str(place_id))

    if place is None:
        abort(404)

    for key, value in body.items():
        if key not in ["id", "city_id", "user_id", "created_at", "updated_at"]:
            setattr(place, key, value)

    storage.save()

    response = jsonify(place.to_dict()), 200

    return response


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending of the JSON in the body
    of the request
    """

    body = request.get_json()

    if not body:
        abort(400, description="Not a JSON")

    if body and len(body):
        states = body.get("states", None)
        cities = body.get("cities", None)
        amenities = body.get("amenities", None)

    if not body or (not states and not cities and not amenities):
        places = storage.all(Place).values()

        places_list = []
        for place in places:
            places_list.append(place.to_dict())
        return jsonify(places_list)

    places_list = []
    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            places_list.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in places_list:
                        places_list.append(place)

    if amenities:
        if not places_list:
            places_list = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]
        places_list = [
            place
            for place in places_list
            if all([am in place.amenities for am in amenities_obj])
        ]

    places = []
    for p in places_list:
        d = p.to_dict()
        d.pop("amenities", None)
        places.append(d)

    return jsonify(places)
