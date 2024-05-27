#!/usr/bin/python3
'''Contains the places view for the API.'''
from os import getenv
from flask import abort, jsonify, make_response, request
import requests
import json
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.state import State
from models.user import User


@app_views.route('cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def get_place(city_id):
    """Return all places in a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    return jsonify([place.to_dict() for place in city.places])


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def single_place(place_id):
    """Return a single place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place(place_id):
    """Delete a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({})


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def post_place(city_id):
    """Add a new place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_place_dict = request.get_json()
    if not new_place_dict:
        abort(400, 'Not a JSON')
    if 'user_id' not in new_place_dict:
        abort(400, "Missing user_id")
    user_id = new_place_dict['user_id']
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if 'name' not in new_place_dict:
        abort(400, "Missing name")
    new_place = Place(**new_place_dict)
    setattr(new_place, 'city_id', city_id)
    storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Update an exist place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")
    for key, value in req.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def places_search():
    """
    retrieves all Place objects depending
    of the JSON in the body of the request
    """
    req = request.get_json()
    if req is None:
        abort(400, "Not a JSON")

    req = request.get_json()
    if req is None or (
        req.get('states') is None and
        req.get('cities') is None and
        req.get('amenities') is None
    ):
        obj_places = storage.all(Place)
        return jsonify([obj.to_dict() for obj in obj_places.values()])

    places = []

    if req.get('states'):
        obj_states = []
        for ids in req.get('states'):
            obj_states.append(storage.get(State, ids))

        for obj_state in obj_states:
            for obj_city in obj_state.cities:
                for obj_place in obj_city.places:
                    places.append(obj_place)

    if req.get('cities'):
        obj_cities = []
        for ids in req.get('cities'):
            add_city = storage.get(City, ids)
            if add_city:
                obj_cities.append(add_city)

        for obj_city in obj_cities:
            for obj_place in obj_city.places:
                if obj_place not in places:
                    places.append(obj_place)

    if not places:
        places = storage.all(Place)
        places = [place for place in places.values()]

    # print("places - amenities \n\n\n")
    # print(places[0].amenities[0])
    if req.get('amenities'):
        print("\n\nfrom amenities\n\n")
        obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
        conf_places = []
        for place in places:
            conf_places.append(place)
            amenities = place.amenities
            for amenity in obj_am:
                if amenity not in amenities:
                    conf_places.pop(-1)
                    break
        places = conf_places
    places = [obj.to_dict() for obj in places]
    return jsonify(places)
# @app_views.route('/places_search', methods=['POST'], strict_slashes=False)
# def places_search():
#     """
#     retrieves all Place objects depending
#     of the JSON in the body of the request
#     """
#     req = request.get_json()
#     if req is None:
#         abort(400, "Not a JSON")

#     req = request.get_json()
#     if req is None or (
#         req.get('states') is None and
#         req.get('cities') is None and
#         req.get('amenities') is None
#     ):
#         obj_places = storage.all(Place)
#         return jsonify([obj.to_dict() for obj in obj_places.values()])

#     places = []

#     if req.get('states'):
#         obj_states = []
#         for ids in req.get('states'):
#             obj_states.append(storage.get(State, ids))

#         for obj_state in obj_states:
#             for obj_city in obj_state.cities:
#                 for obj_place in obj_city.places:
#                     places.append(obj_place)

#     if req.get('cities'):
#         obj_cities = []
#         for ids in req.get('cities'):
#             add_city = storage.get(City, ids)
#             if add_city:
#                 obj_cities.append(add_city)

#         for obj_city in obj_cities:
#             for obj_place in obj_city.places:
#                 if obj_place not in places:
#                     places.append(obj_place)

#     if not places:
#         places = storage.all(Place)
#         places = [place for place in places.values()]

#     if req.get('amenities'):
#         obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
#         i = 0
#         limit = len(places)
#         HBNB_API_HOST = getenv('HBNB_API_HOST')
#         HBNB_API_PORT = getenv('HBNB_API_PORT')

#         port = 5000 if not HBNB_API_PORT else HBNB_API_PORT
#         first_url = "http://0.0.0.0:{}/api/v1/places/".format(port)
#         while i < limit:
#             place = places[i]
#             url = first_url + '{}/amenities'
#             req = url.format(place.id)
#             response = requests.get(req)
#             place_am = json.loads(response.text)
#             amenities = [storage.get(Amenity, obj['id']) for obj in place_am]
#             for amenity in obj_am:
#                 if amenity not in amenities:
#                     places.pop(i)
#                     i -= 1
#                     limit -= 1
#                     break
#             i += 1
#     print(len(places))
#     return jsonify([obj.to_dict() for obj in places])
