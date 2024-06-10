#!/usr/bin/python3
"""
    Handles all default RESTFul API actions for Amenity objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models.amenity import Amenity
from models import storage


@app_views.route("/amenities", strict_slashes=False)
def get_amenities():
    """
        Retrieves the list of Amenity object
    """
    all_amenities = storage.all(Amenity)
    amenities_list = list()
    for amenity in all_amenities.values():
        amenities_list.append(amenity.to_dict())
    return Response(json.dumps(amenities_list, indent=2),
                    mimetype="application/json", status=200)


@app_views.route("/amenities/<amenity_id>", strict_slashes=False)
def get_amenity(amenity_id):
    """
        Retrieves a Amenity object
    """
    all_amenities = storage.all(Amenity)
    for amenity in all_amenities.values():
        if amenity_id == amenity.id:
            return Response(json.dumps(amenity.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)


@app_views.route("/amenities/<amenity_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
        Deletes a Amenity object
    """
    keep_amenity = None
    all_amenities = storage.all(Amenity)
    for key, value in all_amenities.items():
        if amenity_id == value.id:
            keep_amenity = key
            break
    if keep_amenity:
        storage.delete(all_amenities[keep_amenity])
        storage.save()
        return Response(json.dumps({}, indent=2), mimetype="application/json",
                        status=200)
    abort(404)


@app_views.route("/amenities", methods=["POST"],
                 strict_slashes=False)
def post_amenity():
    """
        Creates a Amenity object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    name = data.get("name")
    if not name:
        return "Missing name", 400
    instance = Amenity()
    for key, val in data.items():
        setattr(instance, key, val)
    instance.save()
    return Response(json.dumps(instance.to_dict(), indent=2),
                    mimetype="application/json", status=201)


@app_views.route("/amenities/<amenity_id>", methods=["PUT"],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """
        Updates an Amenity object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    all_amenities = storage.all(Amenity)
    for amenity in all_amenities.values():
        if amenity_id == amenity.id:
            for key, val in data.items():
                if key == "id" or key == "created_at" or key == "updated_at":
                    continue
                setattr(amenity, key, val)
            storage.save()
            return Response(json.dumps(amenity.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)
