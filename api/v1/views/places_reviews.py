#!/usr/bin/python3
"""
Module that handles all default RESTful API actions for
Places/Reviews class
"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    "/places/<place_id>/reviews", methods=["GET"], strict_slashes=False
)
def get_reviews(place_id):
    """retrieves a list of all Review objects of a Place"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    review_list = [review.to_dict() for review in place.reviews]

    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review(review_id):
    """retrieves a review object based on its id"""
    review = storage.get(Review, review_id)

    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route(
    "/places/<place_id>/reviews", methods=["POST"], strict_slashes=False
)
def create_review(place_id):
    """creates a review object and link it to a place object"""
    place = storage.get(Place, place_id)

    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    user_id = body.get("user_id")
    if user_id is None:
        abort(400, "Missing user_id")

    if storage.get(User, user_id) is None:
        abort(404)

    if body.get("text") is None:
        abort(400, "Missing text")

    body["place_id"] = place_id
    new_review = Review(**body)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """updates a review object by id"""
    review = storage.get(Review, review_id)

    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, "Not a JSON")

    body = request.get_json()

    excluded_keys = ["id", "user_id", "place_id" "created_at", "updated_at"]

    for key, value in body.items():
        if key not in excluded_keys:
            setattr(review, key, value)

    review.save()

    return jsonify(review.to_dict()), 200


@app_views.route(
    "/reviews/<review_id>", methods=["DELETE"], strict_slashes=False
)
def delete_review(review_id):
    """deletes a review object by id"""
    review = storage.get(Review, review_id)

    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)
