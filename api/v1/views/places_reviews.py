#!/usr/bin/python3
"""
Creates new view for Place obj that handles all the restful API
"""
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
        '/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_review_by_place(place_id):
    """
    Retrieves a list of all reviews for a specified place
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews_list = []
    for review in place.reviews:
        reviews_list.append(review.to_dict())
    return jsonify(reviews_list)


@app_views.route('/reviews<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    """
    Retrieves a specific review by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    review_json = review.to_dict()
    return jsonify(review_json)


@app_views.route('/review/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a specific review by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """
    Creates a new review
    """
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)  # No valid user
    data['place_id'] = place_id
    review = Review(**data)
    storage.save()
    review_json = review.to_dict()
    return jsonify(review_json), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """
    Updates a specific review by ID
    """
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.is_json:  # check for malformed request
        abort(400, 'Not a JSON')
    data = request.get_json()
    for key, value in data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
