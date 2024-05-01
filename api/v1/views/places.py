#!/usr/bin/python3
"""
route for handling Place objects and operations
"""
from api.v1.views import app_views, storage
from flask import jsonify, abort, request, make_response
from models.city import City
from models.place import Place
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.route("/places_search", methods=["POST"], strict_slashes=False)
def places_search():
    """Retrieves all Place objects based
    on the JSON in the body of the request."""
    try:
        req_data = request.get_json()
        if not req_data:
            # If the JSON body is empty or each list of all keys are empty
            places = storage.all(Place)
        else:
            places = []
            # If states list is not empty
            if "states" in req_data and req_data["states"]:
                for state_id in req_data["states"]:
                    state = storage.get("State", state_id)
                    for city in state.cities:
                        places.extend(city.places)
            # If cities list is not empty
            if "cities" in req_data and req_data["cities"]:
                for city_id in req_data["cities"]:
                    city = storage.get("City", city_id)
                    if city not in places:  # Avoid duplicates
                        places.extend(city.places)
            # If amenities list is not empty
            if "amenities" in req_data and req_data["amenities"]:
                places = [
                    place
                    for place in places
                    if all(
                        amenity in place.amenities
                        for amenity in req_data["amenities"]
                    )
                ]
    except BadRequest:
        # If the HTTP request body is not valid JSON
        abort(400, description="Not a JSON")
    return jsonify([place.to_dict() for place in places])


@app_views.route(
    "/cities/<city_id>/places", methods=["GET"], strict_slashes=False
)
def places_by_city(city_id):
    """
    Retrieve all Place objects associated
    with a specific city from the database.

    This function queries the database for all
    Place objects that are linked to a particular city.
    It returns a JSON-formatted list of Place objects, providing
    a convenient way to access all places within the same city.

    Returns:
    - json: A JSON-formatted list of Place objects for the specified city.
    """
    place_lst = []
    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    for place in city.places:
        place_lst.append(place.to_dict())

    return jsonify(place_lst)


@app_views.route("/places/<place_id>", methods=["GET"], strict_slashes=False)
def get_place(place_id):
    """
    Retrieve a specific Place object by its unique ID.

    This function searches the database for aPlace object that matches the
    provided ID.If the object is found, it is returned in its entirety.
    If no matching Place object is found, an error message is generated
    and returned, indicating that the requested object does not exist.

    Parameters:
    - place_id (int or str): The unique identifier
      of the Place object to retrieve.

    Returns:
    - place: The Place object with the specified ID if found.
    - error: An error message if no Place object
    with the specified ID is found.
    """

    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route(
    "/places/<place_id>", methods=["DELETE"], strict_slashes=False
)
def delete_place(place_id):
    """
    Delete a Place object from the database by its unique ID.

    This function attempts to locate a Place object using the given ID.
    If the object is found, it is removed from the database.
    Upon successful deletion, an empty dictionary is returned along with
    a 200 HTTP status code, signifying a successful operation.
    If the Place object cannot be found, a 404 HTTP status code is returned,
    indicating that the resource was not found.

    Parameters:
    - place_id (int or str): The unique identifier
    of the Place object to be deleted.

    Returns:
    - dict: An empty dictionary if the deletion is successful.
    - int: An HTTP status code of 200 for successful
    deletion or 404 if the Place object is not found.
    """
    place = storage.get(Place, str(place_id))

    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/cities/<city_id>/places", methods=["POST"], strict_slashes=False
)
def create_place(city_id):
    """
    Create a new Place object and store it in the database.

    This function collects the necessary data from the request, constructs a
    new Place object, and persists it to the database.
    It returns the newly created Place object, typically including details
    such as location, description, and any other relevant place information.

    Returns:
    - place: The newly created Place object with
    its attributes populated as per the request data.
    """
    city = storage.get(City, str(city_id))
    if not city:
        abort(404)
    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, description="Missing user_id")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    if "name" not in data:
        abort(400, description="Missing name")
    data["city_id"] = city_id
    new_place = Place(**data)
    new_place.save()
    res = jsonify(new_place.to_dict())
    return make_response(res, 201)


@app_views.route("/places/<place_id>", methods=["PUT"], strict_slashes=False)
def update_place(place_id):
    """
    Update a specific Place object in the database by its unique ID.

    This function locates a Place object using the provided ID and updates
    its information with the data received from the request.
    If the update is successful, the function returns the updated Place object
    along with a 200 HTTP status code.
    If the update fails due to invalid data,
    a 400 HTTP status code is returned.
    If the Place object with the specified ID does not exist,
    a 404 HTTP status code is returned.

    Parameters:
    - place_id (int or str):
        The unique identifier of the Place object to be updated.

    Returns:
    - place: The updated Place object if the update is successful.
    - int: An HTTP status code of 200 for a successful update,
    400 for invalid data, or 404 if the Place object is not found.
    """
    try:
        data = request.get_json(silent=True)
        if data is None:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    ignore_keys = ["id", "created_at", "updated_at", "user_id", "city_id"]
    for key, val in data.items():
        if key not in ignore_keys:
            setattr(place, key, val)
    place.save()
    res = jsonify(place.to_dict())
    return make_response(res, 200)
