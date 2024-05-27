#!/usr/bin/python3
"""places"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.user import User


@app_views.route("/cities/<city_id>/places", methods=["GET"])
@app_views.route("/cities/<city_id>/places/", methods=["GET"])
def list_places_of_city(city_id):
    """Retrieves a list of all Place objects in city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route("/places/<place_id>", methods=["GET"])
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"])
def delete_place(place_id):
    """Deletes a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route("/cities/<city_id>/places", methods=["POST"])
def create_place(city_id):
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()

    user_id = data.get("user_id")
    if not user_id:
        abort(400, description="Missing user_id")

    name = data.get("name")
    if not name:
        abort(400, description="Missing name")

    user = storage.get(User, user_id)
    if not user:
        abort(404)

    new_place = Place(city_id=city_id, user_id=user_id, name=name, **data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def search_places():
    """Searches for Place objects based on the JSON in the request body"""
    if not request.is_json:
        abort(400, description="Not a JSON")

    search_data = request.get_json()

    states = search_data.get('states', [])
    cities = search_data.get('cities', [])
    amenities = search_data.get('amenities', [])

    if not states and not cities:
        places = storage.all(Place).values()
    else:
        places = set()
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        places.update(city.places)
        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    places.update(city.places)

    if amenities:
        amenities_set = set(amenities)
        filtered_places = []
        for place in places:
            place_amenities = {amenity.id for amenity in place.amenities}
            if amenities_set.issubset(place_amenities):
                filtered_places.append(place.to_dict())
        return jsonify(filtered_places)

    return jsonify([place.to_dict() for place in places])


@app_views.route("/places/<place_id>", methods=["PUT"])
def updates_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, description="Not a JSON")

    data = request.get_json()
    ignore_keys = ["id", "user_id", "city_id", "created_at", "updated_at"]

    for key, value in data.items():
        if key not in ignore_keys:
            setattr(place, key, value)

    storage.save()
    return jsonify(place.to_dict()), 200


if __name__ == "__main__":
    pass
