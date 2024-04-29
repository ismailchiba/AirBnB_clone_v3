#!/usr/bin/python3
"""index """

from models import storage
from flask import jsonify, request, abort
from api.v1.views import app_views
from models.place import Place
from models.review import Review


@app_views.route("/places/<place_id>/reviews", methods=['GET', 'POST'])
def places_without_id(place_id=None):
    """Create a new place or return all the cities"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        review_list = []
        review_dict = storage.all(Review)
        for review in review_dict.values():
            if review.place_id == place_id:
                review_list.append(review.to_dict())
        return jsonify(review_list), 200

    if request.method == 'POST':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        if json.get('name') is None:
            abort(400, "Missing name")
        json['place_id'] = place_id
        review = review(**json)
        review.save()
        return jsonify(review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=['GET', 'PUT', 'DELETE'])
def reviews_with_id(review_id=None):
    """Perform READ UPDATE DELETE operations on a place object"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if request.method == 'GET':
        return jsonify(review.to_dict())

    if request.method == 'DELETE':
        review.delete()
        del review
        return jsonify({}), 200

    if request.method == 'PUT':
        json = request.get_json()
        if json is None:
            abort(400, "Not a JSON")
        review.update(**json)
        return jsonify(review.to_dict()), 200
