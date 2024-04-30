#!/usr/bin/python3
"""return JSON """
from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from models.user import User


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def get_reviews():
    review_api = []
    reviews = storage.all(State).values()
    for review in reviews:
        review_api.append(review.to_dict())
    return jsonify(review_api)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review_by_id(review_id):
    review = storage.get(State, review_id)
    if review:
        review_api = review.to_dict()
        return jsonify(review_api)
    else:
        from api.v1.app import not_found
        return not_found(404)


@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review_by_id(review_id):
    review = storage.get(State, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/reviews', methods=['POST'], strict_slashes=False)
def post_review_by_name():
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    if not request.get_json():
        abort(400, 'Not a JSON')

    data_request = request.get_json()
    data = data_request['name']
    obj = State(name=data)
    obj.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def put_review_by_id(review_id):
    if not request.get_json():
        abort(400, 'Not a JSON')
    review = storage.get(State, review_id)
    if review:
        data_request = request.get_json()
        for k, v in data_request.items():
            if k != 'id' and k != 'created_at' and k != 'updated_at':
                setattr(review, k, v)
                storage.save()
        return jsonify(review.to_dict()), 201
    else:
        abort(404)
