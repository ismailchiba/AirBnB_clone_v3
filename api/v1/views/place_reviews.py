#!/usr/bin/python3
"""Reviews route handler"""

from api.v1.views import app_views
from models import storage
from models.review import Review
from models.state import State
from models.place import Place
from models.city import City
from models.user import User
from models.amenity import Amenity
from flask import abort, make_response, request, jsonify


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["GET"])
def place_reviews(place_id):
    """ get reviews by place"""
    reviews = []
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    else:
        for r in place.reviews:
            reviews.append(r.to_dict())
        return jsonify(reviews)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["GET"])
def review(review_id):
    """ get review by id """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_review(review_id):
    """ delete review by id"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        storage.delete(review)
        storage.save()
        return make_response(jsonify({}), 200)


@app_views.route("/places/<place_id>/reviews", strict_slashes=False,
                 methods=["POST"])
def add_review(place_id):
    """ create a review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Not a JSON'}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({'error': 'Missing user_id'}), 400)
    if 'text' not in data:
        return make_response(jsonify({'error': 'Missing text'}), 400)
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    review = Review(**data)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", strict_slashes=False, methods=["PUT"])
def update_review(review_id=None):
    """ Update review data"""
    data = request.get_json()
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    else:
        if not data:
            return make_response(jsonify({'error': 'Not a JSON'}), 400)
        for attr, val in data.items():
            if attr not in ['id', 'user_id', 'place_id', 'created_at',
                            'updated_at']:
                setattr(review, attr, val)
        review.save()
    return make_response(jsonify(review.to_dict()), 200)
