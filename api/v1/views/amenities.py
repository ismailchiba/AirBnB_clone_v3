#!/usr/bin/python3
"""Defines the view functions for managing amenities in the API.

This module handles CRUD operations (Create, Read, Update, Delete)
for amenity objects. It exposes endpoints for fetching all amenities,
retrieving a specific amenity by ID, adding new amenities, and deleting
or updating existing ones.

It utilizes the `storage` module for persistence and raises appropriate
exceptions for invalid requests or resource not found errors.
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


ALLOWED_METHODS = ['GET', 'DELETE', 'POST', 'PUT']
"""List of allowed HTTP methods for the amenities endpoint."""


@app_views.route('/amenities', methods=ALLOWED_METHODS)
@app_views.route('/amenities/<amenity_id>', methods=ALLOWED_METHODS)
def handle_amenities(amenity_id=None):
    """Dispatches incoming requests based on the HTTP method.

    This function acts as a central handler for all amenity-related
    requests. It checks the request method and delegates the processing
    to the appropriate function (get_amenities, remove_amenity, etc.).
    """
    handlers = {
        'GET': get_amenities,
        'DELETE': remove_amenity,
        'POST': add_amenity,
        'PUT': update_amenity,
    }
    if request.method in handlers:
        return handlers[request.method](amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_amenities(amenity_id=None):
    """Retrieves all amenities or a specific amenity by ID.

    If no ID is provided, this function returns a list of all amenity
    objects in JSON format. If an ID is provided, it fetches the
    corresponding amenity object and returns it as JSON, raising a
    NotFound exception if the amenity is not found.
    """
    all_amenities = storage.all(Amenity).values()
    if amenity_id:
        res = list(filter(lambda x: x.id == amenity_id, all_amenities))
        if res:
            return jsonify(res[0].to_dict())
        raise NotFound()
    all_amenities = list(map(lambda x: x.to_dict(), all_amenities))
    return jsonify(all_amenities)


def remove_amenity(amenity_id=None):
    """Deletes a specific amenity by ID.

    This function searches for the amenity with the provided ID and
    attempts to remove it from storage. If the amenity is found, it is
    deleted and a success message is returned. Otherwise, a NotFound
    exception is raised.
    """
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        storage.delete(res[0])
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_amenity(amenity_id=None):
    """Creates a new amenity object.

    This function expects a JSON object containing the amenity data
    (including the 'name' property) in the request body. It validates
    the request data and creates a new Amenity object if everything
    is correct. The new amenity is then saved and returned as JSON.
    BadRequest exceptions are raised for invalid data or missing
    required fields.
    """
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'name' not in data:
        raise BadRequest(description='Missing name')
    new_amenity = Amenity(**data)
    new_amenity.save()
    return jsonify(new_amenity.to_dict()), 201


def update_amenity(amenity_id=None):
    """Updates an existing amenity object.

    This function retrieves the amenity with the provided ID and
    attempts to update its properties based on the data sent in the
    request body (JSON format). It validates the request data and
    ignores attempts to update read-only properties ('id', 'created_at',
    'updated_at'). A NotFound exception is raised if the amenity is not found.
    """
    xkeys = ('id', 'created_at', 'updated_at')
    all_amenities = storage.all(Amenity).values()
    res = list(filter(lambda x: x.id == amenity_id, all_amenities))
    if res:
        data = request.get_json()
        if type(data) is not dict:
            raise BadRequest(description='Not a JSON')
        old_amenity = res[0]
        for key, value in data.items():
            if key not in xkeys:
                setattr(old_amenity, key, value)
        old_amenity.save()
        return jsonify(old_amenity.to_dict()), 200
    raise NotFound()
