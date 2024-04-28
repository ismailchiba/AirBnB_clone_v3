#!/usr/bin/python3
"""review"""
from api.v1.views import app_views
from flask import jsonify, request, abort, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review


@app_views.route(
    'places/<place_id>/reviews',
    methods=['GET'],
    strict_slashes=False
)
def get_reviews(place_id):
    """get all reviews"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    all_reviews = [i.to_dict() for i in place.reviews]
    return jsonify(all_reviews)


@app_views.route(
    '/reviews/<review_id>',
    methods=['GET'],
    strict_slashes=False
)
def get_review(review_id):
    """get review from id"""
    i = storage.get(Review, review_id)
    if i is None:
        abort(404)
    return jsonify(i.to_dict())


@app_views.route(
    '/reviews/<review_id>',
    methods=['DELETE'],
    strict_slashes=False
)
def delete_review(review_id):
    """delete review from id"""
    i = storage.get(Review, review_id)
    if i is None:
        abort(404)
    storage.delete(i)
    storage.save()
    return jsonify({})


@app_views.route(
    '/places/<place_id>/reviews',
    methods=['POST'],
    strict_slashes=False
)
def create_review(place_id):
    """create review"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(jsonify({"error": "Not a JSON"}), 400)
    if 'user_id' not in data:
        return make_response(jsonify({"error": "Missing user_id"}), 400)
    data['place_id'] = place_id
    user = storage.get(User, data['user_id'])
    if user is None:
        abort(404)
    if 'text' not in data:
        return make_response(jsonify({"error": "Missing text"}), 400)
    i = Place(**data)
    i.save()
    return make_response(jsonify(i.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>',
    methods=['PUT'],
    strict_slashes=False
)
def update_review(review_id):
    """update review"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    data = request.get_json()
    if not data:
        return make_response(
            jsonify({"error": "Not a JSON"}), 400
        )
    for k, v in data.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, k, v)
    storage.save()
    return jsonify(review.to_dict())
