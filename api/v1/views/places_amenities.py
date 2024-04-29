#!/usr/bin/python3

"""This module will create a Flask app that serves the content of the AirBnB clone v3 RESTful API.
It retrieves the list of all Amenity objects of a Place
This is the places_amenities view module
And will be imported in the app.py module
"""

from flask import abort, jsonify, make_response
from api.v1.views import app_views
from models import storage
from models import amenity
from models.amenity import Amenity
from models.place import Place
from os import getenv


@app_views.route('/places/<place_id>/amenities',
                 methods=['GET'], strict_slashes=False)
def place_amenities(place_id):
    """This will be called when the route /places/<place_id>/amenities is requested
    It does this by retrieving the list of all Amenity objects of a Place
    So it will return a JSON object with all Amenity objects of a Place
    Retrieves the list of all Amenity objects of a Place"""
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        obj = [amenity.to_dict() for amenity in obj_place.amenities]
    else:
        obj = [storage.get(Amenity, amenity_id).to_dict()
               for amenity_id in obj_place.amenity_ids]
    return jsonify(obj)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_place_amenity(place_id, amenity_id):
    """This function
    Returns an empty dictionary with the status code 200
    It will be called when the route /places/<place_id>/amenities/<amenity_id> is requested with the DELETE method
    And will delete a Amenity object to a Place
    """
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    obj_amenity = storage.get(Amenity, amenity_id)
    if not obj_amenity:
        abort(404)

    for elem in obj_place.amenities:
        if elem.id == obj_amenity.id:
            if getenv('HBNB_TYPE_STORAGE') == 'db':
                obj_place.amenities.remove(obj_amenity)
            else:
                obj_place.amenity_ids.remove(obj_amenity)
            storage.save()
            return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['POST'], strict_slashes=False)
def link_place_amenity(place_id, amenity_id):
    """This function
    Returns the Amenity with the status code 201
    This will be called when the route /places/<place_id>/amenities/<amenity_id> is requested with the POST method
    It will link a Amenity object to a Place
    """
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    obj_amenity = storage.get(Amenity, amenity_id)
    if not obj_amenity:
        abort(404)

    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if obj_amenity in obj_place.amenities:
            return make_response(jsonify(obj_amenity.to_dict()), 200)
        obj_place.amenities.append(obj_amenity)
    else:
        if amenity_id in obj_place.amenity_ids:
            return make_response(jsonify(obj_amenity.to_dict()), 200)
        obj_place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(obj_amenity.to_dict()), 201)
