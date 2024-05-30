#!/usr/bin/python3
"""Module for the  new niew of Reviwe objects"""

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import abort, request, jsonify


@app_views.route("places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def get_reviews(place_id):
    """Retrieves all reviews by place id"""
    reviews_list = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = place.reviews
    for review in reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["GET"])
def get_review_by_id(review_id):
    """Retrieves a review object based on its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict()), 200


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """deletes review based on its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def create_review(place_id):
    """create a new review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data["user_id"])
    if user is None:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    new_review = Review(place_id=place.id, **data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["PUT"])
def update_review(review_id):
    """update review based on its id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict()), 200
