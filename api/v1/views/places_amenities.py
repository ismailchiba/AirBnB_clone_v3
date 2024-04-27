#!/usr/bin/python3
"""
This is module places_amenities
"""
from api.v1.views import (Amenity, app_views, Place, storage)
from flask import (abort, jsonify, make_response, request)
from os import getenv
from sqlalchemy import inspect

if getenv('HBNB_TYPE_STORAGE', 'fs') != 'db':
    # FILE STORAGE
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def view_amenities_in_place(place_id):
        """
        Retrieves a list of all amenties by place_id
        """
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        res = [amen.to_json() for amen in place_obj.amenities]
        return jsonify(res)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id=None, amenity_id=None):
        """
        Deletes a placeamenity based on the place_id and amenity_id
        """
        place_obj = storage.get("Place", place_id)
        if (place_obj is None) or (amenity_id is None):
            abort(404)
        if amenity_id not in place_obj.amenities_id:
            abort(404)
        else:
            place_obj.amenities_id.remove(amenity_id)
            place_obj.save()
            return jsonify({}), 200

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """
        Creates a link based on an amentiy and a place based on the JSON body
        """
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None:
            return "Bad amenity", 404
        if amenity_id in place_obj.amenities_id:
            return jsonify(amenity_obj.to_json()), 200
        place_obj.amenities_id.append(amenity_id)
        place_obj.save()
        return jsonify(amenity_obj.to_json()), 201

else:
    # DB STORAGE
    @app_views.route('/places/<place_id>/amenities', methods=['GET'],
                     strict_slashes=False)
    def view_amenities_in_place(place_id):
        """
        Retrieves a list of all amenties specified by place_id
        """
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        res = [plc.to_json() for plc in place_obj.amenities]
        return jsonify(res)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['DELETE'], strict_slashes=False)
    def delete_placeamenity(place_id=None, amenity_id=None):
        """
        Deletes a placeamenity based on the place_id and amenity_id
        """
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        amenity = storage.get("Amenity", amenity_id)
        if amenity is not None:
            try:
                place_obj.amenities.remove(amenity)
                place_obj.save()
                return jsonify({}), 200
            except ValueError:
                abort(404)
        else:
            abort(404)

    @app_views.route('/places/<place_id>/amenities/<amenity_id>',
                     methods=['POST'], strict_slashes=False)
    def create_amenity_in_place(place_id=None, amenity_id=None):
        """
        Creates a link based on an amentiy and a place.
        """
        place_obj = storage.get("Place", place_id)
        if place_obj is None:
            abort(404)
        amenity_obj = storage.get("Amenity", amenity_id)
        if amenity_obj is None:
            abort(404)
        if amenity_obj in place_obj.amenities:
            return jsonify(amenity_obj.to_json()), 200
        place_obj.amenities.append(amenity_obj)
        place_obj.save()
        return jsonify(amenity_obj.to_json()), 201
