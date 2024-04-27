#!/usr/bin/python3
"""
This is module places
"""
from api.v1.views import (app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
import os


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def view_places_in_city(city_id):
    """
    Retrieves all places within a city
    """
    ct_obj = storage.get("City", city_id)
    if ct_obj is None:
        abort(404)
    rez = [place.to_json() for place in city.places]
    return jsonify(rez)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def view_place(place_id=None):
    """
    Retrieves a place with its id
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    return jsonify(place_obj.to_json())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """
    Deletes a place based on its id.
    """
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    storage.delete(place_obj)
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    ct_obj = storage.get("City", city_id)
    if ct_obj is None:
        abort(404)
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if 'user_id' not in res.keys():
        return "Missing user_id", 400
    user_obj = storage.get("User", res.get("user_id"))
    if user_obj is None:
        abort(404)
    if 'name' not in res.keys():
        return "Missing name", 400
    res["city_id"] = city_id
    new_place = Place(**res)
    new_place.save()
    return jsonify(new_place.to_json()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """
    Updates a place based on the JSON body
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    for item in ("id", "user_id", "city_id", "created_at", "updated_at"):
        res.pop(item, None)
    for key, value in res.items():
        setattr(place_obj, key, value)
    place_obj.save()
    return jsonify(place_obj.to_json()), 200


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def list_places():
    """
    Retrieves a list of all places.
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if not res:
        return jsonify([item.to_json() for item in storage.all("Place").values()])

    cities_id = res.get("cities", [])
    states = res.get("states")
    if states:
        state_list = [storage.get("State", s) for s in states]
        state_list = [st for st in state_list if st is not None]
        cities_id += [ct.id for st in state_list for ct in st.cities]
    cities_id = list(set(cities_id))

    amenities_list = res.get("amenities")
    place_list = []
    if cities_id or amenities_list:
        places = storage.all("Place").values()
        if cities_id:
            places = [plc for plc in places if
                           plc.city_id in cities_id]
        if amenities_list:
            if os.getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
                place_list = [plc for plc in places if
                              set(amenities_list) <= set(plc.amenities_id)]
            else:
                for item in places:
                    flag = True
                    for elem in amenities_list:
                        if elem not in [i.id for i in item.amenities]:
                            flag = False
                            break
                    if flag:
                        place_list.append(e)
        else:
            place_list = places
    return jsonify([p.to_json() for p in place_list])
