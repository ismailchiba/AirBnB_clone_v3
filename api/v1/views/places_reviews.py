#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request, make_response
from api.v1.views import app_views, storage
from models.place import Place
from models.review import Review
from models.user import User
from werkzeug.exceptions import BadRequest


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False
)
def reviews_by_place(place_id):
    """
    Retrieve all Review objects related to a specific place from the database.

    This function queries the database
    for all Review objects that are linked to a particular place.
    It returns a JSON-formatted list of Review objects,
    providing a comprehensive view of all reviews for that place.

    Returns:
    - json: A JSON-formatted list of all
    Review objects associated with the specified place.
    """
    review_list = []
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    for review in place.reviews:
        review_list.append(review.to_dict())
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """
    Retrieve a specific Review object by its unique ID.

    This function searches the database for a Review object that
    matches the provided ID. If the object is found,
    it is returned in its entirety.
    If no matching Review object is found,
    an error message is generated and returned,
    indicating that the requested object does not exist.

    Parameters:
    - review_id (int or str): The unique
    identifier of the Review object to retrieve.

    Returns:
    - review: The Review object with the specified ID if found.
    - error: An error message if no
    Review object with the specified ID is found.
    """
    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def review_delete_by_id(review_id):
    """
    Delete a Review object from the database by its unique ID.

    This function attempts to locate a Review object using the
    given ID. If the object is found, it is removed from the database.
    Upon successful deletion, an empty dictionary is returned along with
    a 200 HTTP status code, signifying a successful operation.
    If the Review object cannot be found, a 404 HTTP status code is returned,
    indicating that the resource was not found.

    Parameters:
    - review_id (int or str): The unique identifier
    of the Review object to be deleted.

    Returns:
    - dict: An empty dictionary if the deletion is successful.
    - int: An HTTP status code of 200 for successful deletion
    or 404 if the Review object is not found.
    """
    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """
    Create a new Review object and store it in the database.

    This function collects the necessary data from the request,
    constructs a new Review object, and saves it to the database.
    It returns the newly created Review object, typically including
    details such as the reviewer's user ID, the place ID,
    the review text, and any associated ratings.

    Returns:
    - review: The newly created Review object
    with its attributes populated as per the request data.
    """
    place = storage.get(Place, str(place_id))
    if not place:
        abort(404)
    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    if "text" not in data:
        abort(400, "Missing text")
    user = storage.get(User, data["user_id"])
    if not user:
        abort(404)
    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()
    res = jsonify(new_review.to_dict())
    return make_response(res, 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def review_put(review_id):
    """
    Update a specific Review object in the database by its unique ID.

    This function locates a Review object using the provided ID and
    updates its information with the data received from the request.
    If the update is successful, the function returns the updated
    Review object along with a 200 HTTP status code.
    If the update fails due to invalid data, a 400 HTTP status code
    is returned. If the Review object with the specified ID does not exist,
    a 404 HTTP status code is returned.

    Parameters:
    - review_id (int or str): The unique identifier
    of the Review object to be updated.

    Returns:
    - review: The updated Review object if the update is successful.
    - int: An HTTP status code of 200 for a successful update,
    400 for invalid data, or 404 if the Review object is not found.
    """
    review = storage.get(Review, str(review_id))
    if not review:
        abort(404)
    try:
        data = request.get_json(silent=True)
        if not data:
            abort(400, "Not a JSON")
    except BadRequest:
        abort(400, "Not a JSON")

    ignore_keys = [
        "id",
        "created_at",
        "updated_at",
        "user_id",
        "place_id",
    ]
    for key, val in data.items():
        if key not in ignore_keys:
            setattr(review, key, val)

    review.save()
    res = jsonify(review.to_dict())
    return make_response(res, 200)
