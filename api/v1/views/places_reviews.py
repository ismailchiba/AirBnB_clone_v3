#!/usr/bin/python3

"""this module will create a view for the Review objects that handles all default RestFul API actions
it will be imported in the __init__.py module
this is the places_reviews view module
and will be used to create a blueprint object that handles all views for the application
"""

from flask import abort, jsonify, make_response, request
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def review(place_id):
    """This function
    Retrieves the list of all Review objects of a Place
    It will be called when the route /places/<place_id>/reviews is requested
    """
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)
    return jsonify([obj.to_dict() for obj in obj_place.reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def single_review(review_id):
    """This function
    It will be called when the route /reviews/<review_id> is requested
    ITS used to 
    Retrieves a Review object
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    return jsonify(obj.to_dict())


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def del_review(review_id):
    """This function
    Deletes a Review object
    It will be called when the route /reviews/<review_id> is requested with the DELETE method
    Deletes a Review object
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)
    obj.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def push_review(place_id):
    """This function
    It will be called when the route /places/<place_id>/reviews is requested with the POST method
    It is used to
    Create a Review object
    """
    obj_place = storage.get(Place, place_id)
    if not obj_place:
        abort(404)

    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    obj_user = storage.get(User, user_id)
    if not obj_user:
        abort(404)
    if 'text' not in new_review:
        abort(400, "Missing text")

    obj = Review(**new_review)
    setattr(obj, 'place_id', place_id)
    storage.new(obj)
    storage.save()
    return make_response(jsonify(obj.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def put_review(review_id):
    """This function
    Updates a Review object
    It will be called when the route /reviews/<review_id> is requested with the PUT method
    """
    obj = storage.get(Review, review_id)
    if not obj:
        abort(404)

    req = request.get_json()
    if not req:
        abort(400, "Not a JSON")

    for k, v in req.items():
        if k not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(obj, k, v)

    storage.save()
    return make_response(jsonify(obj.to_dict()), 200)
