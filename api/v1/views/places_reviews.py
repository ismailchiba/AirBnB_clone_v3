#!/usr/bin/python3
"""this file adds HTTP methods for the Review class"""

import json
from models import storage
from api.v1.views import app_views
from flask import Flask, request, jsonify, abort, make_response
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def get_place_reviews(place_id):
    """Gets a list of all cities of a specific state"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, description="Place not found")

    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict()) in place.reviews
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """Deletes a specific review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    storage.delete(review)
    storage.save()
    return jsonify({}), 200


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def post_review(place_id):
    """Creates a new Place under a specific City"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")
    if 'place_id' not in data:
        abort(400, description="Missing place_id")

    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    new_review = User(**data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def put_place(place_id):
    """Updates a specific place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    data = request.get_json(force=True)
    if not data:
        abort(400, description="Not a JSON")

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at', 'user_id']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


if __name__ == '__main__':
    app_views.run(debug=True)
