#!/usr/bin/python3
"""
route for handling Review objects and operations
"""
from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """
    retrieves all Review objects by place
    """
    review_list = []
    place_object = storage.get("Place", str(place_id))

    if place_object is None:
        abort(404)

    for obj in place_object.reviews:
        review_list.append(obj.to_json())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    create review route
    """
    review_json = request.get_json(silent=True)
    if review_json is None:
        abort(400, 'Not a JSON')
    if not storage.get("Place", place_id):
        abort(404)
    if not storage.get("User", review_json["user_id"]):
        abort(404)
    if "user_id" not in review_json:
        abort(400, 'Missing user_id')
    if "text" not in review_json:
        abort(400, 'Missing text')

    review_json["place_id"] = place_id

    new_review = Review(**review_json)
    new_review.save()
    response = jsonify(new_review.to_json())
    response.status_code = 201

    return response


@app_views.route("/reviews/<review_id>",  methods=["GET"],
                 strict_slashes=False)
def review_by_id(review_id):
    """
    gets a specific review object by ID
    """

    fetched_object = storage.get("Review", str(review_id))

    if fetched_object is None:
        abort(404)

    return jsonify(fetched_object.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def reviewUodate_by_id(review_id):
    """
    updates specific Review object by ID
    return: Review object and 200 on success, or 400 or 404 on failure
    """
    place_json = request.get_json(silent=True)

    if place_json is None:
        abort(400, 'Not a JSON')

    fetched_object = storage.get("Review", str(review_id))

    if fetched_object is None:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(fetched_object, key, value)

    fetched_object.save()

    return jsonify(fetched_object.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"],
                 strict_slashes=False)
def review_delete_by_id(review_id):
    """
    deletes Review by id
    """

    fetched_object = storage.get("Review", str(review_id))

    if fetched_object is None:
        abort(404)

    storage.delete(fetched_object)
    storage.save()

    return jsonify({})
