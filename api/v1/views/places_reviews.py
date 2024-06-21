from flask import jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route('/places/<place_id>/reviews', methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    if 'user_id' not in request_data:
        abort(400, "Missing user_id")
    user = storage.get(User, request_data['user_id'])
    if not user:
        abort(404)
    if 'text' not in request_data:
        abort(400, "Missing text")
    request_data['place_id'] = place_id
    new_review = Review(**request_data)
    storage.new(new_review)
    storage.save()
    return jsonify(new_review.to_dict()), 201


@app_views.route('/reviews/<review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    request_data = request.get_json()
    if not request_data:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
