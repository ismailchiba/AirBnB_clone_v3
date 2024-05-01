#!/usr/bin/python3
"""Defines the view for places amenities Api calls"""
import os
from flask import abort, jsonify, request, make_response
from flasgger import swag_from
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route("/places/<place_id>/amenities", methods=["GET"])
def place_amenities(place_id):
    """Defines the GET method for getting a list of amenities"""
    place = storage.get("Place", place_id)

    if place is None:
        abort(404)
    return jsonify([a.to_dict() for a in place.amenities])


@app_views.route(
    "/places/<place_id>/amenities/<amenity_id>",
    methods=["POST", "DELETE"]
)
def post_delete_place_amenities(place_id, amenity_id):
    """Defines the POST and DELETE methods for a Amenity object"""
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    exists = False
    if place is None or amenity is None:
        abort(404)

    if request.method == "POST":
        if os.getenv("HBNB_TYPE_STORAGE") == "db":
            if amenity in place.amenities:
                exists = True
            else:
                place.amenities.append(amenity)
        else:
            if amenity.id in place.amenity_ids:
                exists = True
            else:
                place.amenity_ids.append(amenity.id)

        place.save()
        return make_response(jsonify(amenity.to_dict()), (200 if exists else 201))

    if os.getenv("HBNB_TYPE_STORAGE") == "db":
        if amenity not in place.amenities:
            abort(404)
        place.amenities.remove(amenity)
    else:
        if amenity.id not in place.amenity_ids:
            abort(404)
        place.amenity_ids.remove(amenity.id)
    place.save()
    return make_response(jsonify({}), 200)
