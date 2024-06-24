#!/usr/bin/python3
""" View for review object """

from flask import request, abort, jsonify, make_response
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_all_reviews(place_id):
    """ Retrieves all review for a place object """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    list_reviews = []
    for review in place.reviews:
        list_reviews.append(review.to_dict())
    return jsonify(list_reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """ Get a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """ Delete a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """ Create a review """
    response = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if response is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in response:
        abort(400, 'Missing user_id')
    user = storage.get(User, response['user_id'])
    if user is None:
        abort(404)
    if 'text' not in response:
        abort(400, 'Missing text')
    response['place_id'] = place_id
    new_review = Review(**response)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """ Update a review """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    response = request.get_json()
    if response is None:
        abort(400, 'Not a JSON')
    keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key, value in response.items():
        if key not in keys:
            setattr(review, key, value)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
