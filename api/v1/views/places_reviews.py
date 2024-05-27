#!/usr/bin/python3
"""
Routes for handling Review objects and operations.
"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves all Review objects by place ID.
    """
    review_list = [review.to_json() for review in storage.get("Place", place_id).reviews]
    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """
    Creates a new Review object.
    """
    review_json = request.get_json(silent=True)
    if not review_json:
        abort(400, 'Not a JSON')

    if "user_id" not in review_json:
        abort(400, 'Missing user_id')

    if "text" not in review_json:
        abort(400, 'Missing text')

    if not storage.get("Place", place_id):
        abort(404)

    if not storage.get("User", review_json["user_id"]):
        abort(404)

    review_json["place_id"] = place_id
    new_review = Review(**review_json)
    new_review.save()
    return jsonify(new_review.to_json()), 201


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a specific Review object by ID.
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    Updates a specific Review object by ID.
    """
    review_json = request.get_json(silent=True)
    if not review_json:
        abort(400, 'Not a JSON')

    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    for key, value in review_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id", "place_id"]:
            setattr(review, key, value)

    review.save()
    return jsonify(review.to_json())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object by ID.
    """
    review = storage.get("Review", review_id)
    if not review:
        abort(404)

    storage.delete(review)
    storage.save()
    return jsonify({}), 200
