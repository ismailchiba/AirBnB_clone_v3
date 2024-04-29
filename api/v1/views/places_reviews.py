#!/usr/bin/python3
"""Module for the API."""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """Get all reviews by specific place id."""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)

    review_list = [review.to_dict() for review in place_by_id.reviews]
    return make_response(jsonify(review_list), 200)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Get review by id."""
    if review_id is None:
        abort(404)
    review_by_id = storage.get(Review, review_id)
    if not review_by_id:
        abort(404)
    return make_response(jsonify(review_by_id.to_dict()), 200)


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """Delete a review by id."""
    review_by_id = storage.get(Review, review_id)
    if not review_by_id:
        abort(404)
    review_by_id.delete()
    review_by_id.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Create a new review."""
    place_by_id = storage.get(Place, place_id)
    if not place_by_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in request.get_json():
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in request.get_json():
        return make_response(jsonify({'error': 'Missing text'}), 400)
    user_by_id = storage.get(User, request.get_json()['user_id'])
    if not user_by_id:
        abort(404)
    new_review = Review(**request.get_json())
    new_review.place_id = place_id
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """Update a review by id."""
    review_by_id = storage.get(Review, review_id)
    if not review_by_id:
        abort(404)
    if not request.get_json():
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    for key, value in request.get_json().items():
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review_by_id, key, value)
    review_by_id.save()
    return make_response(jsonify(review_by_id.to_dict()), 200)
