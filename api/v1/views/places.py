#!/usr/bin/python3
"""
Route for handling Place objects and operations.
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.place import Place


@app_views.route("/cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def places_by_city(city_id):
    """
    retrieves all Place objects by city

    :param city_id: ID of the city
    :return: JSON of all Places
    """
    # Initialize empty list to store the Place objects
    place_list = []

    # Get the City object with the specified ID
    city_obj = storage.get("City", str(city_id))

    # Iterate over the places attribute of the City object
    for obj in city_obj.places:
        # Append the JSON representation of each Place object to the list
        place_list.append(obj.to_json())

    # Return the list as a JSON response
    return jsonify(place_list)


@app_views.route("/cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def place_create(city_id):
    """
    Create a new Place object

    :param city_id: ID of the city the Place belongs to
    :return: Newly created Place object as a JSON response
    """
    # Get the JSON data from the request
    place_json = request.get_json(silent=True)

    # Check if the request is a valid JSON
    if place_json is None:
        abort(400, 'Not a JSON')

    # Check if the User and City objects with the specified IDs exist
    if not storage.get("User", place_json["user_id"]):
        abort(404)
    if not storage.get("City", city_id):
        abort(404)

    # Check if the required fields are present in the JSON data
    if "user_id" not in place_json:
        abort(400, 'Missing user_id')
    if "name" not in place_json:
        abort(400, 'Missing name')

    # Add the city_id to the JSON data
    place_json["city_id"] = city_id

    # Create a new Place object using the JSON data
    new_place = Place(**place_json)
    new_place.save()

    # Return the JSON representation of the new Place object as a response
    resp = jsonify(new_place.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/places/<place_id>",  methods=["GET"],
                 strict_slashes=False)
def place_by_id(place_id):
    """
    Get a specific Place object by ID

    :param place_id: ID of the Place object
    :return: Place object with the specified ID as a JSON response
    """
    # Get the Place object with the specified ID
    fetched_obj = storage.get("Place", str(place_id))

    # Check if the Place object exists
    if fetched_obj is None:
        abort(404)

    # Return the JSON representation of the Place object as a response
    return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["PUT"],
                 strict_slashes=False)
def place_put(place_id):
    """
    Update a specific Place object by ID

    :param place_id: ID of the Place object
    :return: Place object with the specified ID as a JSON response, or 400 or 404 on failure
    """
    # Get the JSON data from the request
    place_json = request.get_json(silent=True)

    # Check if the request is a valid JSON
    if place_json is None:
        abort(400, 'Not a JSON')

    # Get the Place object with the specified ID
    fetched_obj = storage.get("Place", str(place_id))

    # Check if the Place object exists
    if fetched_obj is None:
        abort(404)

    # Update the attributes of the Place object with the values from the JSON data
    for key, val in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "city_id"]:
            setattr(fetched_obj, key, val)

    # Save the changes to the Place object
    fetched_obj.save()

    # Return the JSON representation of the updated Place object as a response
    return jsonify(fetched_obj.to_json())


@app_views.route("/places/<place_id>",  methods=["DELETE"],
                 strict_slashes=False)
def place_delete_by_id(place_id):
    """
    Delete a Place object by ID

    :param place_id: ID of the Place object
    :return: Empty dict as a JSON response with 200 on success, or 404 if not found
    """
    # Get the Place object with the specified ID
    fetched_obj = storage.get("Place", str(place_id))

    # Check if the Place object exists
    if fetched_obj is None:
        abort(404)

    # Delete the Place object from storage
    storage.delete(fetched_obj)
    storage.save()

    # Return an empty JSON response
    return jsonify({})

