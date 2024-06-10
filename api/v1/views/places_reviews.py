#!/usr/bin/python3
"""Contains the places_reviews view for the API.

This module handles endpoints for managing reviews associated with places.
It offers functionalities to:

* Retrieve all reviews belonging to a specific place.
* Get a single review by its unique identifier.
* Create a new review for a place, requiring a user ID and text content.
* Delete an existing review.
* Update the details of a review (excluding read-only attributes).
"""
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest

from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET', 'POST'])
@app_views.route('/reviews/<review_id>', methods=['GET', 'DELETE', 'PUT'])
def handle_reviews(place_id=None, review_id=None):
    """Dispatches incoming requests based on the HTTP method.

    This function acts as a central handler for all review-related
    requests. It checks the request method and delegates the processing
    to the appropriate function (get_reviews, remove_review, etc.).
    """

    handlers = {
        'GET': get_reviews,
        'DELETE': remove_review,
        'POST': add_review,
        'PUT': update_review
    }
    if request.method in handlers:
        return handlers[request.method](place_id, review_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_reviews(place_id=None, review_id=None):
    """Retrieves all reviews associated with a place or a single review.

    If a place ID is provided, this function returns a JSON list containing
    all review objects linked to that place. If a review ID is provided,
    it fetches and returns the corresponding review object as JSON. A
    NotFound exception is raised if the place or review is not found.
    """
    if place_id:
        place = storage.get(Place, place_id)
        if place:
            reviews = []
            for review in place.reviews:
                reviews.append(review.to_dict())
            return jsonify(reviews)
    elif review_id:
        review = storage.get(Review, review_id)
        if review:
            return jsonify(review.to_dict())
    raise NotFound()


def remove_review(place_id=None, review_id=None):
    """Deletes a review.

    This function searches for the review with the provided ID and attempts
    to remove it from storage. If the review is found, it is deleted and
    a success message is returned. A NotFound exception is raised if the
    review is not found.
    """
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    raise NotFound()


def add_review(place_id=None, review_id=None):
    """Creates a new review for a place.

    This function expects a POST request to `/places/<place_id>/reviews`
    containing a JSON object with the following properties:

    * user_id: The ID of the user creating the review (required).
    * text: The content of the review (required).

    It verifies the existence of the referenced place and user before
    proceeding. A NotFound exception is raised if either the place or
    user is not found.  A BadRequest exception is raised if the request
    body is not JSON or if the required properties (`user_id` or `text`)
    are missing. Upon successful creation of the review, it is saved to
    storage and a JSON response containing the newly created review object
    is returned with a 201 Created status code.
    """
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    data = request.get_json()
    if type(data) is not dict:
        raise BadRequest(description='Not a JSON')
    if 'user_id' not in data:
        raise BadRequest(description='Missing user_id')
    user = storage.get(User, data['user_id'])
    if not user:
        raise NotFound()
    if 'text' not in data:
        raise BadRequest(description='Missing text')
    data['place_id'] = place_id
    new_review = Review(**data)
    new_review.save()
    return jsonify(new_review.to_dict()), 201


def update_review(place_id=None, review_id=None):
    """Updates an existing review.

    This function allows updating the details of a review identified by
    its ID. It expects a PUT request to `/reviews/<review_id>` containing
    a JSON object with properties to be modified. It ignores attempts to
    update read-only attributes (`id`, `user_id`, `place_id`, `created_at`,
    `updated_at`). A NotFound exception is raised if the review is not
    found. A BadRequest exception is raised if the request body is not
    JSON. Upon successful update, the review is saved to storage and a
    JSON response containing the updated review object is returned with
    a 200 OK status code.
    """
    xkeys = ('id', 'user_id', 'place_id', 'created_at', 'updated_at')
    if review_id:
        review = storage.get(Review, review_id)
        if review:
            data = request.get_json()
            if type(data) is not dict:
                raise BadRequest(description='Not a JSON')
            for key, value in data.items():
                if key not in xkeys:
                    setattr(review, key, value)
            review.save()
            return jsonify(review.to_dict()), 200
    raise NotFound()
