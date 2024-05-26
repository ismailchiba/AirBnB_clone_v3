#!/usr/bin/python3
""" It creates a new view for Review objects"""

from flask import Flask
from flask import Flask, abort
from api.v1.views import app_views
from os import name
from models.state import State, City
from flask import request


@app_views.route('/places'/<string:place_id>/reviews, methods=['GET'] strict_slashes=False)
def retrieves_all_reviews():
    """It retrieves all reviews of places otherwise raises an error."""
    reviewsObject = storage.get('Place', 'place_id')
    list = []
    for review in reviewsObject.values():
        if reviewsObject is None:
        abort(404)
        list.append(review.to_dict())
    return jsonify(list)


@app_views.route('/reviews/<string:review_id>', methods=['GET'],
                 strict_slashes=False)
def get_a_review():
    """It retrieves a review otherwise raises an error."""
    reviewsObject = storage.get('Review', 'review_id')
    if reviewsObject is None:
        abort(404)
    return jsonify(reviewsObject.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'],
                 strict_slashes=False)
def deletes_user():
    """ It deletes a Review otherwise raises an error."""
    reviewsObject = storage.get('Review', 'review_id')
    if reviewsObject is None:
        abort(404)
    storage.delete(reviewsObject)
    storage.save()
    return jsonify({}), '200'


@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def creates-user():
    """It creates a Review."""

    response = request.get_json()
    placesObject = storage.get('Place', 'place_id')
    usersObject = storage.get('User', 'user_id')
    if placesObject is None:
        abort(404)
    if response is None:
        abort(400, {'Not a JSON'})
    if "user_id" not in response:
        abort(400, {'Missing user_id'})
    if usersObject is None:
        abort(404)
    if "text" not in response:
        abort(400, {'Missing text'})

    placesObject = Review(__tablename__=response['__tablename__'])
    storage.new(placesObject)
    storage.save()
    return jsonify(placesObject.to_dict()), '201'


@app_views.route('/reviews/<string:review_id>', methods=['PUT'],
                 strict_slashes=False)
def updates_user():
    """It updates a Review."""

    response = request.get_json()
    reviewsObject = storage.get('Review', 'review_id')

    if reviewsObject is None:
        abort(404)
    if response is None:
        abort(400, {'Not a JSON'})
    ignoreKeys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for key in response.items():
        if key not in ignoreKeys:
            setattr(reviewsObject, key)
    storage.save()
    return jsonify(reviewsObject.to_dict()), '200'
