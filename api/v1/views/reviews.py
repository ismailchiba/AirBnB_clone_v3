#!/usr/bin/python3
""" objects that handles all default RestFul API actions for Reviews"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models.place import Place
from models import storage
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"], strict_slashes=False)
def get_review(place_id):
    """Retrieves the list of all Review objects"""
    place = storage.get(Place, place_id)

    if not place:
        abort(404)

    reviews = [review.to_dict() for review in place.reviews]

    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"], strict_slashes=False)
def get_review_id(review_id):
    """Retrieves a Review by id"""
    review = storage.get(review, review_id)
    if not review:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"], strict_slashes=False)
def delete_review_id(review_id):
    """Deletes a Review object by id"""
    review = storage.get(review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """Creates a Review"""
    place = storage.get(Place, place_id)

    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data["user_id"])

    if not user:
        abort(404)

    if "name" not in request.get_json():
        abort(400, description="Missing name")

    data["place_id"] = place_id
    instance = Place(**data)
    instance.save()
    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by id"""
    if not request.get_json():
        abort(400, description="Not a JSON")
    if not storage.get(review, review_id):
        abort(404)

    review = storage.get(review, review_id)
    review_data = request.get_json()
    ignore_keys = ["id", "created_at", "updated_at"]
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)
    storage.save()

    return make_response(jsonify(review.to_dict()), 200)
