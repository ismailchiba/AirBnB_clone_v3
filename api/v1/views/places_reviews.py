#!/usr/bin/python3
"""RESTFul API actions for Review object"""


from api.v1.views import app_views, jsonify
from models.place import Place
from models.review import Review
from models.user import User
from models import storage
from flask import abort, request


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Retrieves the list of all Review objects of a Place"""
    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    list_reviews = []
    # reviews_obj = storage.all(Review)
    for obj in place_obj.reviews:
        list_reviews.append(obj.to_dict())
    return jsonify(list_reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    return jsonify(review_obj.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object"""
    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    storage.delete(review_obj)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """Creates a new Review object for a Place"""

    place_obj = storage.get(Place, place_id)

    if not place_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")
    if "user_id" not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user_id = data.get("user_id")

    user_obj = storage.get(User, user_id)

    if not user_obj:
        abort(404)

    if "text" not in request.get_json():
        abort(400, description="Missing text")

    data["place_id"] = place_id
    new_review = Review(**data)
    new_review.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object"""

    review_obj = storage.get(Review, review_id)

    if not review_obj:
        abort(404)

    if not request.get_json():
        abort(400, description="Not a JSON")

    data = request.get_json()

    for key, value in data.items():
        if key not in\
                ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(review_obj, key, value)

    storage.save()
    return jsonify(review_obj.to_dict()), 200
