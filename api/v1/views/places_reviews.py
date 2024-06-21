#!/usr/bin/python3
"""python doc
"""
from flask import jsonify, request, abort
from models import storage
from models.state import State
from models.review import Review
from models.city import City
from models.place import Place
from models.user import User
from api.v1.views import app_views


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['GET'])
def listOfReview(place_id):
    """A list of review objects"""
    places = storage.get(Place, place_id)
    if places is None:
        return abort(404)
    rev = [rv.to_dict() for rv in places.reviews]
    return jsonify(rev)


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['GET'])
def getRevById(review_id):
    """Get the review"""
    rev = storage.get(Review, review_id)
    if rev is None:
        return abort(404)
    return jsonify(rev.to_dict())


@app_views.route('/places/<place_id>/reviews',
                 strict_slashes=False, methods=['POST'])
def createRev(place_id):
    """create a review for a certain place"""
    place = storage.get(Place, place_id)
    if not place:
        return abort(404)
    try:
        data = request.get_json()
    except BadRequest:
        return abort(400, 'Not a JSON')
    if not data:
        return abort(400, 'Not a JSON')
    if 'user_id' not in data.keys():
        return abort(400, 'Missing user_id')
    user_id = data.get("user_id")
    user = storage.get(User, user_id)
    if not user:
        return abort(404)
    if 'text' not in data.keys():
        return abort(400, 'Missing text')
    rev = Review(place_id=place_id, **data)
    storage.new(rev)
    storage.save()
    return jsonify(rev.to_dict()), 201


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['PUT'])
def UpdateReview(review_id):
    """Update that review"""
    rev = storage.get(Review, review_id)
    if not rev:
        return abort(404)
    try:
        data = request.get_json()
    except BadRequest:
        return abort(400, 'Not a JSON')
    if not data:
        return abort(400, 'Not a JSON')
    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']
    for k, v in data.items():
        if k not in ignore:
            setattr(rev, k, v)
    rev.save()
    return jsonify(rev.to_dict()), 200


@app_views.route('/reviews/<review_id>',
                 strict_slashes=False, methods=['DELETE'])
def deleteReview(review_id):
    """"delete specific id"""
    rev = storage.get(Review, review_id)
    if not rev:
        return abort(404)
    storage.delete(rev)
    storage.save()
    return jsonify({}), 200
