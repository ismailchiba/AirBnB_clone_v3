#!/usr/bin/python3
"""Defines the view functions for managing place-amenity relationships.

This module handles endpoints for managing the association between
place and amenity objects. It allows:

* Retrieving all amenities associated with a specific place using a GET
  request to `/places/<place_id>/amenities`.
* Removing an existing association between a place and an amenity using
  a DELETE request to `/places/<place_id>/amenities/<amenity_id>`.
* Creating a new association between a place and an amenity using a
  POST request to `/places/<place_id>/amenities/<amenity_id>`.

It considers the storage type (`db` or file-based) when handling
relationship management to ensure data consistency.
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST']
)
def handle_places_amenities(place_id=None, amenity_id=None):
    """Dispatches incoming requests based on the HTTP method.

    This function acts as a central handler for all place-amenity
    relationship related requests. It checks the request method and
    delegates the processing to the appropriate function (get_place_amenities,
    remove_place_amenity, etc.).
    """

    handlers = {
        'GET': get_place_amenities,
        'DELETE': remove_place_amenity,
        'POST': add_place_amenity
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_place_amenities(place_id=None, amenity_id=None):
    """Retrieves all amenities associated with a specific place.

    This function takes a place ID and returns a JSON list containing
    all amenity objects linked to that place. A NotFound exception is
    raised if the place is not found.
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            all_amenities = list(map(lambda x: x.to_dict(), place.amenities))
            return jsonify(all_amenities)
    raise NotFound()


def remove_place_amenity(place_id=None, amenity_id=None):
    """Removes an amenity association from a place.

    This function removes the association between a place and an amenity
    given their respective IDs. It verifies the existence of both the
    place and amenity objects before proceeding. If the storage type is
    'db' (relational database), it also handles the many-to-many
    relationship management at the database level. Otherwise, it updates
    the place's 'amenity_ids' list. A NotFound exception is raised if
    either the place or amenity is not found, or if the association
    does not exist.
    """
    if place_id and amenity_id:
        place = storage.get(Place, place_id)
        if not place:
            raise NotFound()
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            raise NotFound()
        place_amenity_link = list(
            filter(lambda x: x.id == amenity_id, place.amenities)
        )
        if not place_amenity_link:
            raise NotFound()
        if storage_t == 'db':
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, amenity.place_amenities)
            )
            if not amenity_place_link:
                raise NotFound()
            place.amenities.remove(amenity)
            place.save()
            return jsonify({}), 200
        else:
            amenity_idx = place.amenity_ids.index(amenity_id)
            place.amenity_ids.pop(amenity_idx)
            place.save()
            return jsonify({}), 200
    raise NotFound()


def add_place_amenity(place_id=None, amenity_id=None):
    """Associates an amenity with a place.

    This function creates a new association between a place and an amenity.
    It checks for the existence of both place and amenity objects before
    proceeding. If the storage type is 'db', it handles the many-to-many
    relationship management at the database level by checking for existing
    associations. Otherwise, it updates the place's 'amenity_ids' list to
    reflect the new association. A NotFound exception is raised if either
    the place or amenity is not found. It returns a 200 status code if
    the association already exists, or a 201 status code if a new
    association is created.
    """
    if place_id and amenity_id:
        place = storage.get(Place, place_id)
        if not place:
            raise NotFound()
        amenity = storage.get(Amenity, amenity_id)
        if not amenity:
            raise NotFound()
        if storage_t == 'db':
            place_amenity_link = list(
                filter(lambda x: x.id == amenity_id, place.amenities)
            )
            amenity_place_link = list(
                filter(lambda x: x.id == place_id, amenity.place_amenities)
            )
            if amenity_place_link and place_amenity_link:
                res = amenity.to_dict()
                del res['place_amenities']
                return jsonify(res), 200
            place.amenities.append(amenity)
            place.save()
            res = amenity.to_dict()
            del res['place_amenities']
            return jsonify(res), 201
        else:
            if amenity_id in place.amenity_ids:
                return jsonify(amenity.to_dict()), 200
            place.amenity_ids.push(amenity_id)
            place.save()
            return jsonify(amenity.to_dict()), 201
    raise NotFound()
