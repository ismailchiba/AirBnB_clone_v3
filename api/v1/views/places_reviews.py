#!/usr/bin/python3
"""
This module defines Flask routes to provide API endpoints
for Review objects.
"""
from flask import abort, jsonify, make_response, request

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User

api_route_1 = "/places/<string:place_id>/reviews"
api_route_2 = "/reviews/<string:review_id>"


@app_views.route(api_route_1, methods=["GET"], strict_slashes=False)
def get_place_reviews(place_id):
    """
    Retrieves the list of all Review objects of a Place
    """

    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    reviews_list = []

    for review in place.reviews:
        reviews_list.append(review.to_dict())

    response = jsonify(reviews_list), 200

    return response


@app_views.route(api_route_1, methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """
    Create a new review.

    Returns:
        tuple: A tuple containing the JSON representation
        of the new review and the HTTP status code 201.
    """
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    body = request.get_json(silent=True)
    review_fields = ["user_id", "text"]

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    for field in review_fields:
        if field not in body:
            message = "Missing {}".format(field)
            return make_response(jsonify({"error": message}), 400)

    body["place_id"] = place_id
    user = storage.get(User, body["user_id"])

    if not user:
        abort(404)

    new_review = Review(**body)

    new_review.save()

    response = jsonify(new_review.to_dict()), 201

    return make_response(response)


@app_views.route(api_route_2, methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a Review object
    """

    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    response = jsonify(review.to_dict()), 200

    return response


@app_views.route(api_route_2, methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    Delete a review by its ID.

    Args:
        review_id (str): The ID of the review to delete.

    Returns:
        tuple: An empty dictionary and the HTTP status code 200.

    Raises:
        404: If the review with the specified ID does not exist.
    """
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return jsonify({})


@app_views.route(api_route_2, methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    Update a review by its ID.

    Args:
        review_id (str): The ID of the review to update.

    Returns:
        tuple: A tuple containing the JSON representation
        of the updated review and the HTTP status code 200.

    Raises:
        404: If the review with the specified ID does not exist.
    """
    body = request.get_json(silent=True)

    if not body:
        return make_response(jsonify({"error": "Not a JSON"}), 400)

    review = storage.get(Review, str(review_id))

    if review is None:
        abort(404)

    for key, value in body.items():
        field = ["id", "user_id", "place_id", "created_at", "updated_at"]
        if key not in field:
            setattr(review, key, value)

    storage.save()

    response = jsonify(review.to_dict()), 200

    return response
