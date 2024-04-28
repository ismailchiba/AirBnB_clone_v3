#!/usr/bin/python3

"""REST API routes for places objects"""

from models.city import City
from models.place import Place
from models.user import User
from models import storage
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views


# GET REQUEST


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def read_places(city_id):
    """ Retrieves place objects corresponding to city id"""
    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    places_list = [place.to_dict() for place in storage.all(Place).values()
                   if place.city_id == city_id]
    return jsonify(places_list)


# GET REQUEST


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def read_place(place_id):
    """Retrieves a place object"""
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    return jsonify(place_obj)


# DELETE REQUEST


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """ This deletes a place object"""

    place_obj = storage.get(City, place_id)

    if not place_obj:
        abort(404)

    # deletes a place
    storage.delete(place_obj)
    storage.save()
    return jsonify({}), 200


# CREAT REQUEST
@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """ This creates a place object """

    city_obj = storage.get(City, city_id)

    if not city_obj:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    http_to_dict = request.get_json()

    if 'user_id' not in http_to_dict:
        abort(400, "Missing user_id")

    user_obj = storage.get(User, http_to_dict['user_id'])

    if not user_obj:
        abort(404)

    if 'name' not in http_to_dict:
        abort(400, "Missing name")

    # Add the city Id into the dictionary if not exist
    http_to_dict['city_id'] = city_id
    new_place_obj = City(**http_to_dict)
    storage.new(new_place_obj)
    storage.save()  # add the object to the storage

    return jsonify(new_place_obj.to_dict()), 201  # return the new object


# UPDATE REQUEST


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id):
    """ This updates a place object"""
    place_obj = storage.get(City, place_id)

    if not place_obj:
        abort(404)

    if not request.get_json():
        abort(400, "Not a JSON")

    http_to_json = request.get_json()

    for key, value in http_to_json.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place_obj, key, value)  # update the object

    storage.save()

    return jsonify(place_obj.to_dict()), 200
