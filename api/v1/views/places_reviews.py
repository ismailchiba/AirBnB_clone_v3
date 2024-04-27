#!/usr/bin/python3
'''Handles Review RESTful API actions'''

from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import request, abort, jsonify


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'],
                 strict_slashes=False)
def all_reviews(place_id):
    '''gets and creates objects of Review object'''
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if request.method == 'GET':
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    if request.method == 'POST':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        if 'user_id' not in body:
            abort(400, 'Missing user_id')
        user = storage.get(User, body['user_id'])
        if not user:
            abort(404)
        if 'text' not in body:
            abort(400, 'Missing text')
        review = Review(**body)
        review.place_id = place_id
        storage.new(review)
        storage.save()
        return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'],
                 strict_slashes=False)
def reviews_by_id(review_id):
    '''gets, deletes, and updates objects of Review object'''
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        body = request.get_json()
        if not body:
            abort(400, 'Not a JSON')
        for key in body.keys():
            if key not in ['id', 'user_id', 'place_id',
                           'created_at', 'updated_at']:
                setattr(review, key, body[key])
        storage.save()
        return jsonify(review.to_dict()), 200
