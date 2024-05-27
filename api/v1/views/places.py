#!/usr/bin/python3
'''Contains the places view for the API.'''
from flask import abort, jsonify, make_response, request
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
#             obj_cities.append(storage.get(City, ids))

#         for obj_city in obj_cities:
#             if obj_city:
#                 for obj_place in obj_city.places:
#                     if obj_place not in places:
#                         places.append(obj_place)

#     if not places:
#         places = storage.all(Place)
#         places = [place for place in places.values()]

#     print("places - amenities \n\n\n")
#     print(places[0].amenities[0])
#     if req.get('amenities'):
#         print("\n\nfrom amenities\n\n")
#         obj_am = [storage.get(Amenity, id) for id in req.get('amenities')]
#         conf_places = []
#         for place in places:
#             conf_places.append(place)
#             amenities = place.amenities
#             for amenity in obj_am:
#                 if amenity not in amenities:
#                     conf_places.pop(-1)
#                     break
#         places = conf_places
#     places = [obj.to_dict() for obj in places]
#     conf_places = [type(obj) for obj in places]
#     print(conf_places)
#     return jsonify(places)

@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """Searches for a place"""
    params = request.get_json()
    if params is None:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)

    states = params.get('states', [])
    cities = params.get('cities', [])
    amenities = params.get('amenities', [])

    places = set()

    # If no states and cities are provided, retrieve all places
    if not states and not cities:
        places = set(storage.all(Place).values())
    else:
        if states:
            for state_id in states:
                state = storage.get(State, state_id)
                if state:
                    for city in state.cities:
                        if city.id not in cities:
                            cities.append(city.id)

        if cities:
            for city_id in cities:
                city = storage.get(City, city_id)
                if city:
                    for place in city.places:
                        places.add(place)

    # Filter places by amenities
    if amenities:
        filtered_places = []
        amenity_objects = [storage.get(Amenity, amenity_id)
                           for amenity_id in amenities
                           if storage.get(Amenity, amenity_id)]
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            amenities_places = [amenity.to_dict()
                                for amenity in place.amenities]
        else:
            amenities_places = [storage.get(Amenity, amenity_id).to_dict()
                                for amenity_id in place.amenity_ids]
        for place in places:
            if all(amenity in amenities_places for amenity in amenity_objects):
                filtered_places.append(place)
    else:
        filtered_places = list(places)

    return jsonify([place.to_dict() for place in filtered_places])
