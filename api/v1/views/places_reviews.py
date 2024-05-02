#!/usr/bin/python3

"""Interact with the Review model"""

from flask import Flask as F, abort, jsonify, request as RQ
from api.v1.views import app_views as AV
from models import storage
from models.review import Review
from models.base_model import BaseModel as BM


reviews = F(__name__)


@AV.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
def get_or_create_reviews(place_id=None):
    """Get all reviews / Create a new review w no Id"""
    Place = storage.get('Place', place_id)
    if Place is None:
        abort(404, 'Not found')

    if RQ.method == 'GET':
        places = storage.all('Place')
        response = [review.to_dict() for review in places.values()
                    if review.place_id == place_id]
        status = 200

    if RQ.method == 'POST':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('text') is None:
            abort(400, 'Missing text')
        user_Id = RQ_json.get('user_id')
        if user_Id is None:
            abort(400, 'Missing user_id')
        if storage.get('User', user_Id) is None:
            abort(404, 'Not found')

        new_user = Review(**RQ_json)
        new_user.save()
        response = new_user.to_dict()
        status = 201
    return jsonify(response), status


@AV.route('/reviews/<review_id>', methods=['GET', 'PUT', 'DELETE'])
def get_del_put_place(review_id=None):
    """Get, delete or update a Review object w a given identifier"""
    response = {}
    review = storage.get('Review', review_id)
    if review is None:
        abort(404, "Not found")

    if RQ.method == 'GET':
        response = review.to_dict()
        status = 200

    if RQ.method == 'PUT':
        RQ_json = RQ.get_json()
        if RQ_json is None:
            abort(400, 'Not a JSON')
        if RQ_json.get('text') is None:
            abort(400, 'Missing text')
        user_Id = RQ_json.get('user_id')
        if user_Id is None:
            abort(400, 'Missing user_id')
        if storage.get('User', user_Id) is None:
            abort(404, 'Not found')

        review = Review.db_update(RQ_json)
        review.save()   # type: ignore
        response = review.to_dict()   # type: ignore
        status = 200

    if RQ.method == 'DELETE':
        review.delete()   # type: ignore
        del review
        status = 200
    return jsonify(response), status
