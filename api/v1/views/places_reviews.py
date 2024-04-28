#!/usr/bin/python3
"""
Route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews_by_place(place_id):
    """
    Retrieves all Review objects by place
    :return: JSON of all reviews
    """
    review_list = []
    place_obj = storage.get("Place", str(place_id))

    if place_obj is None:
        abort(404)

    for review in place_obj.reviews:
        review_list.append(review.to_json())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create Review route
    :return: Newly created Review object
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')
    if not storage.get("User", review_json["user_id"]):
        abort(404)

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    resp = jsonify(new_review.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def get_review_by_id(review_id):
    """
    Gets a specific Review object by ID
    :param review_id: Review object ID
    :return: Review object with the specified ID or error
    """

    fetched_review = storage.get("Review", str(review_id))

    if fetched_review is None:
        abort(404)

    return jsonify(fetched_review.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """
    Updates specific Review object by ID
    :param review_id: Review object ID
    :return: Review object and 200 on success, or 400 or 404 on failure
    """
    review_json = request.get_json(silent=True)

    if review_json is None:
        abort(400, 'Not a JSON')

    fetched_review = storage.get("Review", str(review_id))

    if fetched_review is None:
        abort(404)

    for key, val in review_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetched_review, key, val)

    fetched_review.save()

    return jsonify(fetched_review.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    """
    Deletes Review by ID
    :param review_id: Review object ID
    :return: Empty dict with 200 or 404 if not found
    """

    fetched_review = storage.get("Review", str(review_id))

    if fetched_review is None:
        abort(404)

    storage.delete(fetched_review)
    storage.save()

    return jsonify({})
