#!/usr/bin/python3
"""
Module creates an api view for Place objects
"""

from flask import jsonify, abort, request
from api.v1.views.__init__ import app_views
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def city_to_place_index(city_id):
    """
    Retrieves all places under city city_id on
    GET /api/v1/cities/<city_id>/places
    """
    parent_obj = storage.get(City, city_id)
    if parent_obj is None:
        abort(404)
    else:
        all_places_raw = parent_obj.places
        all_places = []
        for place in all_places_raw:
            all_places.append(place.to_dict())
        return jsonify(all_places)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def place_by_id(place_id):
    """
    Retrieves place object by its id on
    GET /api/v1/places/<place_id>
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        return jsonify(obj.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """
    Deletes a place object on
    DELETE /api/v1/places/<place_id> request
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200


@app_views.route("/places/<place_id>", methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """
    Replaces a place object on
    PUT /api/v1/places/<place_id> request
    """
    obj = storage.get(Place, place_id)
    if obj is None:
        abort(404)

    else:
        content_type = request.headers.get('Content-Type')
        if content_type != 'application/json':
            abort(400, description='Not a JSON')
        else:
            json = request.get_json()
            if json is None:
                abort(400, description='Not a JSON')
            for key, value in json.items():
                if key not in [
                    'id', 'user_id', 'city_id', 'created_at', 'updated_at'
                ]:
                    setattr(obj, key, value)
                obj.save()
            return place_by_id(place_id), 200


@app_views.route("/cities/<city_id>/places", methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """
    Posts a place object and adds it to its parent city
    POST /api/v1/cities/<city_id>/places request
    """
    parent_obj = storage.get(City, city_id)
    if parent_obj is None:
        abort(404)

    content_type = request.headers.get('Content-Type')
    if content_type != 'application/json':
        abort(400, description='Not a JSON')
    else:
        json = request.get_json()
        if json is None:
            abort(400, description='Not a JSON')
        if 'name' not in json.keys():
            abort(400, description='Missing name')
        elif 'user_id' not in json.keys():
            abort(400, description='Missing user_id')

        all_users = list(storage.all(User).values())
        all_user_ids = list(user.id for user in all_users)

        if json['user_id'] not in all_user_ids:
            abort(404)
        else:
            obj = Place(**json)
            obj.city_id = city_id
            obj_id = obj.id
            obj.save()
            return place_by_id(obj_id), 201
