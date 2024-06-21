#!/usr/bin/python3

from flask import Blueprint, jsonify, abort, request, make_response
from werkzeug.exceptions import BadRequest
from models import storage
from models.review import Review
from models.place import Place
from models.user import User

app_places_reviews = Blueprint("app_places_reviews", __name__)


def get_object_by_id(cls, obj_id):
    """ This function is used to retrive a specific object using its id
    """
    for _, obj in storage.all(cls).items():
        if obj.id == obj_id:
            return obj
    return None


@app_places_reviews.route("/<place_id>/reviews", methods=['GET'])
def retrive_reviews_of_place(place_id):
    """ This function return list of all reviews related to a place
    """
    place = get_object_by_id(Place, place_id)
    if not place:
        abort(404)
    return [review.to_dict() for review in place.places]


@app_places_reviews.route("/<review_id>", methods=['GET'])
def retrive_review(review_id):
    """ This function is used to retrive a specific review
        object using its id
    """
    review = get_object_by_id(Review, review_id)
    if not review:
        abort(404)
    return review.to_dict()


@app_places_reviews.route("/<review_id>", methods=['DELETE'])
def delete_review(review_id):
    """ This function is used to delete an review object when
        the DELETE method is called
    """
    review = get_object_by_id(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return {}, 200


@app_places_reviews.route("/<place_id>/reviews", methods=['POST'])
def create_review(place_id):
    """ This function creates a new review object
    """
    place = get_object_by_id(Place, place_id)
    if place is None:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    if 'user_id' not in request_data:
        abort(400, description="Missing user_id")

    user_id = request_data['user_id']
    user = get_object_by_id(User, user_id)
    if user is None:
        abort(404)

    if 'text' not in request_data:
        abort(400, description="Missing text")

    new_review = Review()
    new_review.text = request_data['text']
    new_review.user_id = user_id
    new_review.place_id = place_id
    new_review.save()
    return new_review.to_dict(), 201


@app_places_reviews.route("/<review_id>", methods=['PUT'])
def update_city(review_id):
    """ This function updates an existing review object
    """
    review = get_object_by_id(Review, review_id)
    if not review:
        abort(404)
    try:
        request_data = request.get_json()
    except BadRequest:
        abort(400, description="Not a JSON")

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at',
                       'city_id', 'place_id'):
            setattr(review, key, value)

    review.save()
    return review.to_dict(), 200
