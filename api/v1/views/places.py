#!/usr/bin/python3
""" Create a new view for Place objects that handles all
    default RESTFul API actions"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def allPlaces(city_id):
    '''Retrieves the list of all City objects of a State:
    GET /api/v1//places/<place_id>'''

    allCities = storage.get('City', city_id)
    listPlaces = []
    if allCities:
        for place in allCities.places:
            listPlaces.append(place.to_dict())
        return jsonify(listPlaces)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def objPlace(place_id):
    '''Retrieves a Place object. :
    GET /api/v1//places/<place_id>'''
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletePlace(place_id):
    '''Deletes a Place object:
    DELETE /api/v1//places/<place_id>'''
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return make_response(jsonify({})), 200
    else:
        abort(404)


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def createUser(city_id):
    '''Creates a PLace'''
    city = storage.get(City, city_id)
    data_request = request.get_json()
    if city:
        if city.get('user_id') is None:
            abort(400, 'Missing user_id')
        if city.get('name') is None:
            abort(400, 'Missing name')
        if city.get('email') is None:
                abort(400, 'Missing email')
        if city.get('password') is None:
            abort(400, 'Missing password')
        newUser = User(**dataRequest)
        storage.new(newUser)
        storage.save()
        return jsonify(newUser.to_dict()), 201
    else:
        abort(400)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def updatePlace(place_id):
    '''Updates a Amenity object:
    PUT /api/v1/amenities/<amenity_id>'''
    obj = storage.get(Place, place_id)
    if obj:
        data_request = request.get_json()
        if isinstance(data_request, dict):
            noKeys = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']
            for key, value in data_request.items():
                if key not in noKeys:
                    setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        else:
            abort(400, 'Not a JSON')
    else:
        abort(404)
