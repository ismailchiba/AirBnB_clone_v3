#!/usr/bin/python3
"""
    Handles all default RESTFul API actions for Review objects
"""
from api.v1.views import app_views
from flask import abort, request, Response
import json
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", strict_slashes=False)
def get_reviews(place_id):
    """
        Retrieves the list of all Review objects of a Place
    """
    all_reviews = storage.all(Review)
    review_list = list()
    for review in all_reviews.values():
        if place_id == review.place_id:
            review_list.append(review.to_dict())
    if review_list:
        return Response(json.dumps(review_list, indent=2),
                        mimetype="application/json", status=200)
    abort(404)


@app_views.route("/reviews/<review_id>", strict_slashes=False)
def get_review(review_id):
    """
        Retrieves a Review object
    """
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review_id == review.id:
            return Response(json.dumps(review.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
        Deletes a Review object
    """
    all_reviews = storage.all(Review)
    keep_review = None
    for key, val in all_reviews.items():
        if review_id == val.id:
            keep_review = key
            break
    if keep_review:
        storage.delete(all_reviews[keep_review])
        storage.save()
        return Response(json.dumps({}, indent=2),
                        mimetype="application/json", status=200)
    abort(404)


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def post_review(place_id):
    """
        Creates a Review object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    user_id = data.get("user_id")
    if not user_id:
        return "Missing user_id", 400
    text = data.get("text")
    if not text:
        return "Missing text", 400
    all_users = storage.all(User)
    keep_user = None
    for user in all_users.values():
        if user_id == user.id:
            keep_user = user
            break
    if not keep_user:
        abort(404)
    all_places = storage.all(Place)
    for place in all_places.values():
        if place_id == place.id:
            instance = Review()
            for key, val in data.items():
                setattr(instance, key, val)
            instance.place_id = place_id
            instance.save()
            return Response(json.dumps(instance.to_dict(), indent=2),
                            mimetype="application/json", status=201)
    abort(404)


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def put_review(review_id):
    """
        Updates a Review object
    """
    try:
        data = request.get_json()
    except Exception:
        return "Not a JSON", 400
    all_reviews = storage.all(Review)
    for review in all_reviews.values():
        if review_id == review.id:
            for key, val in data.items():
                if key == "id" or key == "user_id" or \
                   key == "place_id" or key == "created_at" or \
                   key == "updated_at":
                    continue
                setattr(review, key, val)
            storage.save()
            return Response(json.dumps(review.to_dict(), indent=2),
                            mimetype="application/json", status=200)
    abort(404)
