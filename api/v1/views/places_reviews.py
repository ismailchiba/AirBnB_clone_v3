#!/usr/bin/python3
"""handle Review operation"""

from flask import jsonify, abort, request
from api.v1.views import app_views, storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def reviews_by_place(place_id):
    """retrieves all Review objects by place"""
    review_list = []
    place_obj = storage.get("Place", str(place_id))
    if place_obj is None:
        abort(404)
    for obj in place_obj.reviews:
        review_list.append(obj.to_json())

    return jsonify(review_list)


@app_views.route("/places/<place_id>/reviews", methods=["POST"], strict_slashes=False)
def review_create(place_id):
    """create  a new REview by its id"""
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
    resp = jsonify(new_review.to_json())
    resp.status_code = 201

    return resp


@app_views.route("/reviews/<review_id>",  methods=["GET"], strict_slashes=False)
def get_review_by_id(review_id):
    """gets a specific review by its id"""
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)
    return jsonify(review_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["PUT"],
                 strict_slashes=False)
def put_review_by_id(review_id):
    """updates specific using its specific id"""
    place_json = request.get_json(silent=True)
    if place_json is None:
        abort(400, 'Not a JSON')
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)

    for key, value in place_json.items():
        if key not in ["id", "created_at", "updated_at", "user_id",
                       "place_id"]:
            setattr(review_obj, key, value)
    review_obj.save()
    return jsonify(review_obj.to_json())


@app_views.route("/reviews/<review_id>",  methods=["DELETE"], strict_slashes=False)
def review_delete_id(review_id):
    """deletes specific Review using its id"""
    review_obj = storage.get("Review", str(review_id))
    if review_obj is None:
        abort(404)
    storage.delete(review_obj)
    storage.save()

    return jsonify({})
