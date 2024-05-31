#!/usr/bin/python3
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.base_model import BaseModel
from models.review import Review
from models.place import Place
from models.user import User
from models import storage


""" reviews views module - GET/PUT/POST/DELETE methods"""


@app_views.route("/places/<place_id>/reviews")
@app_views.route("/places/<place_id>/reviews/")
def get_reviews(place_id):
    """ return reviews of a given <place_id> """

    valid_place = False
    for place in storage.all(Place).values():
        if place.id == place_id:
            valid_place = True
            break
    if valid_place is False:
        abort(404)

    reviews = []
    for review in storage.all(Review).values():
        if review.place_id == place_id:
            reviews.append(review.to_dict())

    return jsonify(reviews), 200


@app_views.route("/reviews/<review_id>")
@app_views.route("/reviews/<review_id>/")
def get_review(review_id):
    """ retrieve review"""

    for review in storage.all(Review).values():
        if review.id == review_id:
            return jsonify(review.to_dict()), 200

    abort(404)


@app_views.route("/reviews/<review_id>", methods=['DELETE'])
@app_views.route("/reviews/<review_id>/", methods=['DELETE'])
def delete_review(review_id):
    """ delete review object"""

    for review in storage.all(Review).values():
        if review.id == review_id:
            storage.delete(review)
            storage.save()
            return jsonify({}), 200

    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=['POST'])
@app_views.route("/places/<place_id>/reviews/", methods=['POST'])
def create_review(place_id):
    """ create review object belonging to a <place_id>"""

    valid_place = False
    for place in storage.all(Place).values():
        if place.id == place_id:
            valid_place = True
            break
    if valid_place is False:
        print("---missing -- plce --")
        abort(404)

    review = request.get_json()
    if review is None:
        abort(400, "NOT a JSON")
    if "user_id" not in review.keys():
        abort(400, "Missing user_id")
    valid_user = False
    for user in storage.all(User).values():
        if user.id == review["user_id"]:
            valid_user = True
    if valid_user is False:
        abort(404)
    if "text" not in review.keys():
        abort(400, "Missing text")

    review["place_id"] = place_id

    new_review = Review(**review)
    storage.new(new_review)
    storage.save()
    return jsonify(review), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"])
@app_views.route("/reviews/<review_id>/", methods=["PUT"])
def review_update(review_id):
    """ update review """

    skip_keys = ["id", "user_id", "review_id", "created_at", "updated_at"]
    for review in storage.all(Review).values():
        if review.id == review_id:
            update_info = request.get_json()
            if update_info is None:
                abort(400, "Not a JSON")
            review_dict = review.to_dict()
            storage.delete(review)
            storage.save()

            for key, value in update_info.items():
                if key not in skip_keys:
                    review_dict[key] = value
            updated_review = Review(**review_dict)
            storage.new(updated_review)
            storage.save()
            return jsonify(review_dict), 200

    abort(404)
