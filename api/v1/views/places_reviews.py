#!/usr/bin/python3
"""
A module for Place_reviews.
"""
from api.v1.views import (app_views, Review, storage)
from flask import (abort, jsonify, request)


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def all_reviews(place_id):
    """
    Retrieves a list of all reviews of a place
    """
    plc_obj = storage.get("Place", place_id)
    if plc_obj is None:
        abort(404)
    review_list = [review.to_json() for review in plc_obj.reviews]
    return jsonify(review_list)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def one_review(review_id):
    """
    Retrieves a review for a place
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_json())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_one_review(review_id):
    """
    Deletes a review based on the place_id
    """
    review_obj = storage.get("Review", review_id)
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Creates one review associated with a place_id
    """
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    if "user_id" not in res.keys():
        return "Missing user_id", 400
    if "text" not in res.keys():
        return "Missing text", 400
    place_obj = storage.get("Place", place_id)
    if place_obj is None:
        abort(404)
    user_obj = storage.get("User", r["user_id"])
    if user_obj is None:
        abort(404)
    rev = Review(**res)
    rev.place_id = place_id
    rev.save()
    return jsonify(rev.to_json()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    Creates one review associated with a place_id
    """
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    try:
        res = request.get_json()
    except Exception as e:
        res = None
    if res is None:
        return "Not a JSON", 400
    for item in ("id", "user_id", "place_id", "created_at", "updated_at"):
        res.pop(item, None)
    for key, val in res.items():
        setattr(review, key, val)
    review.save()
    return jsonify(review.to_json()), 200
