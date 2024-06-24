#!/usr/bin/python3
"""
view for Place objects that handles
all default RESTFul API actions
"""
from api.v1.views import app_views
from flask import abort, request, jsonify
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State


@app_views.route("/cities/<city_id>/places", methods=['GET'],
                 strict_slashes=False)
def retrive_places_by_city(city_id):
    """ This function return list of places users """
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([place.to_dict() for place in city.places])


@app_views.route(
        "/places/<place_id>",
        methods=['GET'],
        strict_slashes=False)
def retrive_place(place_id):
    """ This function is used to retrive a specific place
        object using its id
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
        "/places/<place_id>",
        methods=['DELETE'],
        strict_slashes=False)
def delete_place(place_id):
    """ This function is used to delete a place object when
        the DELETE method is called
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ This function creates a new place object
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    if 'user_id' not in request_data:
        abort(400, "Missing user_id")

    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)

    if 'name' not in request_data:
        abort(400, "Missing name")

    # request_data['city_id'] = city_id
    new_place = Place(city_id=city_id, **request_data)
    new_place.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """ This function updates an existing place object
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json(silent=True)
    if not request_data:
        abort(400, "Not a JSON")

    for key, value in request_data.items():
        if key not in ['id', 'created_at', 'updated_at', 'city_id', 'user_id']:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route("/places_search", methods=['POST'],
                 strict_slashes=False)
def search_places():
    """ This function hadles route to places_search """
    cities = []
    places_list = []
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")

    if not request_data or all(not li for li in request_data.values()):
        return jsonify([place for place in storage.all(Place).values()])

    if "states" in request_data:
        for state in request_data["states"]:
            for city in storage.get(State, state).cities:
                cities.append(city.id)

    if "cities" in request_data:
        for city_id in request_data["cities"]:
            if city_id not in cities:
                cities.append(city_id)

    for city_id in cities:
        city = storage.get(City, city_id)
        if not city:
            continue
        places = city.places
        for place in places:
            places_list.append(place)

    if "amenities" in request_data:
        amenities_list = request_data["amenities"]
        tmp_list = places_list.copy()
        for place in tmp_list:
            done = 1
            for amenitie in place.amenities:
                if done == 0:
                    break
                if amenitie.id not in amenities_list:
                    places_list.remove(place)
                    done = 0
                    

    return jsonify([place.to_dict() for place in places_list])
