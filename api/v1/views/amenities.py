#!/usr/bin/python3
""" Module contains view/routes for amenities """

from models.amenity import Amenity
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """ returns all amenities json """
    amenities = storage.all("Amenity").values()
    amenities_list = [amenity.to_dict() for amenity in amenities]
    return jsonify(amenities_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """ return amenity with an id <amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    else:
        return jsonify([amenity.to_dict()])


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ deletesn an amenity with an id <amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    else:
        storage.delete(amenity)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route('/amenities', methods=['POST'],
                 strict_slashes=False)
def add_amenity():
    """ Adds an amenity """
    if request.is_json:
        kwargs_data = request.get_json()
        if 'name' not in kwargs_data:
            abort(400, description="Missing name")
        amenity = Amenity(**kwargs_data)
        amenity.save()
        return make_response(jsonify(amenity.to_dict()), 200)
    abort(400)

@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """ updates an amenity with an id <amenity_id> """
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    else:
        if request.is_json:
            kwargs_data = request.get_json()
            for key, val in kwargs_data.items():
               setattr(amenity, key, val)
            storage.save()
            return make_response(jsonify(amenity.to_dict()), 200)
        abort(400, description='Not a JSON')   