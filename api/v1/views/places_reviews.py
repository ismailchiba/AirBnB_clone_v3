#!/usr/bin/python3
"""
defines api for accessing Review objects
"""
from flask import jsonify, abort, request
from . import app_views
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('places/<place_id>/reviews', methods=['GET'])
@app_views.route('places/<place_id>/reviews/', methods=['GET'])
def get_place_reviews(place_id):
    """
    Retrieves list of all Review objects of a Place
    """
    place = storage.get(Place, place_id)
    reviews = []
    if not place:
        abort(404)
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'])
def get_review_obj(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>', methods=['DELETE'])
def delete_review_obj(review_id):
    """Deletes a Review object"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('places/<place_id>/reviews', methods=['POST'])
@app_views.route('places/<place_id>/reviews/', methods=['POST'])
def create_place_review_obj(place_id):
    """ Creates a Review object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    data = request.get_json()
    if not data:
        abort(404, "Not a JSON")
    if "user_id" not in data:
        abort(400, "Missing user_id")
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)
    if "text" not in data:
        abort(400, "Missing text")
    if not data.get("place_id"):
        review = Review(**data, place_id=place_id)
        storage.new(review)
    else:
        review = Review(**data)
        storage.new(review)
    storage.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'])
def update_review_obj(review_id):
    """
    Updates a Review object
    """
    data = request.get_json()
    if not data:
        abort(400, "Not a JSON")
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    for key, val in data.items():
        if hasattr(review, key):
            setattr(review, key, val)
    storage.save()
    return jsonify(review.to_dict()), 200
