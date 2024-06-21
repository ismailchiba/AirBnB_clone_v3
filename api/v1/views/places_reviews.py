#!/usr/bin/python3
"""API Review view."""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=["GET", "POST"])
def reviews(place_id):
    """Defines the GET and POST method for reviews on /places route."""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    if request.method == "GET":
        return jsonify([r.to_dict() for r in place.reviews])

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    user_id = data.get("user_id")
    if user_id is None:
        return "Missing user_id", 400
    if storage.get("User", user_id) is None:
        abort(404)
    if data.get("text") is None:
        return "Missing text", 400
    data["place_id"] = place_id
    review = Review(**data)
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["GET", "DELETE", "PUT"])
def review_id(review_id):
    """Defines the GET, PUT and DELETE methods for a specific ID."""
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)

    if request.method == "GET":
        return jsonify(review.to_dict())

    elif request.method == "DELETE":
        storage.delete(review)
        storage.save()
        return jsonify({})

    data = request.get_json(silent=True)
    if data is None:
        return "Not a JSON", 400
    avoid = {"id", "user_id", "place_id", "created_at", "updated_at"}
    [setattr(review, k, v) for k, v in data.items() if k not in avoid]
    review.save()
    return jsonify(review.to_dict())
