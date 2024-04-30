#!/usr/bin/python3

"""
This  is a view for the Review object that handles all
default RESTFul API action (CRUD)
"""

from flask import make_response, jsonify, abort, request
from models import storage
from models.review import Review
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews', strict_slashes=False)
def get_reviews_of_place(place_id):
    """
    This method retrieves the list of all Review object of
    a Place with the specified place_id
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    place_reviews = [review.to_dict() for review in place.reviews]

    return jsonify(place_reviews)


@app_views.route('/reviews/<review_id>', strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object with the specified review_id
    """

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=["DELETE"], strict_slashes=False)
def delete_review(review_id):
    """
    This method deletes a Review object with the
    specified review_id
    """

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    storage.delete(review)
    storage.save()

    return make_response({}, 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=["POST"], strict_slashes=False)
def create_review(place_id):
    """
    This method creates a Review object
    """

    place = storage.get("Place", place_id)

    if place is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    if 'user_id' not in request_body:
        abort(404, description='Missing user_id')

    user = storage.get("User", request_body.get('user_id'))

    if user is None:
        abort(404)

    if 'text' not in request_body:
        abort(400, description='Missing text')

    request_body['place_id'] = place_id

    new_review = Review(**request_body)
    storage.new(new_review)
    storage.save()

    return make_response(new_review.to_dict(), 201)


@app_views.route('/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def update_review(review_id):
    """
    This method updates a Review object with the
    specified review_id
    """

    review = storage.get("Review", review_id)

    if review is None:
        abort(404)

    if not request.is_json:
        abort(400, description='Not a JSON')

    request_body = request.get_json()

    for key, value in request_body.items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, value)

    review.save()
    return make_response(review.to_dict(), 200)
