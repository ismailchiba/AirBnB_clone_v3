#!/usr/bin/python3
"""
Defines API routes for handling Place reviews objects
"""
from flask import abort, jsonify, request
from models.review import Review
from models.place import Place
from models.user import User
from api.v1.views import app_views
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews_of_place(place_id):
    """
    Retrieves the list of all Review objects of a Place: GET /api/v1/places/<place_id>/reviews
    If the place_id is not linked to any Place object, raise a 404 error
    """
    place = storage.get('Place', place_id)
    if not place:
         abort(404)

    reviews = [review.to_dict() for review in place.reviews]
    return jsonify(reviews)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """
    Retrieves a Review object. : GET /api/v1/reviews/<review_id>
    If the review_id is not linked to any Review object, raise a 404 error
    """
    review = storage.get('Review', review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """
    Deletes a Review object: DELETE /api/v1/reviews/<review_id>
    If the review_id is not linked to any Review object, raise a 404 error
    Returns an empty dictionary with the status code 200
    """
    review = storage.get('Review', review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """
    Creates a Review: POST /api/v1/places/<place_id>/reviews
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the place_id is not linked to any Place object, raise a 404 error
    If the HTTP body request is not valid JSON, raise a 400 error with the message Not a JSON
    If the dictionary doesn’t contain the key user_id, raise a 400 error with the message Missing user_id
    If the user_id is not linked to any User object, raise a 404 error
    If the dictionary doesn’t contain the key text, raise a 400 error with the message Missing text
    Returns the new Review with the status code 201
    """
    place = storage.get('Place', place_id)
    if not place:
        abort(404)

    if not request.is_json:
        abort(400, 'Not a JSON')

    data = request.get_json()
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    if 'text' not in data:
        abort(400, 'Missing text')
    
    user = storage.get('User', data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """
    Updates a Review object: PUT /api/v1/reviews/<review_id>
    If the review_id is not linked to any Review object, raise a 404 error
    You must use request.get_json from Flask to transform the HTTP request to a dictionary
    If the HTTP request body is not valid JSON, raise a 400 error with the message Not a JSON
    Update the Review object with all key-value pairs of the dictionary
    Ignore keys: id, user_id, place_id, created_at and updated_at
    Returns the Review object with the status code 200
    """
    review = storage.get('Review', review_id)
    if review:
        if not request.is_json:
            abort(400, 'Not a JSON')
        data = request.get_json()
        ignore_keys = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
        for key, value in data.items():
            if key not in ignore_keys:
                setattr(review, key, value)

        review.save()
        return jsonify(review.to_dict()), 200
    else:
        abort(404)
