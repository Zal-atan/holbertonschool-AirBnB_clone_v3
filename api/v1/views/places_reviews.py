#!/usr/bin/python3
""" Review API calls module """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews', methods=["GET"], strict_slashes=False)
def reviews_getter(place_id):
    """ List all Review objects of a Place """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if place is None:
        abort(404)
    list_reviews = [review.to_dict() for review in place.reviews]
    return jsonify(list_reviews)


@app_views.route(
    '/reviews/<review_id>', methods=["GET"], strict_slashes=False)
def specific_review_getter(review_id):
    """ Retrieves data of a specific Review from ID """
    specific_review = storage.get(Review, review_id)
    if specific_review is None:
        abort(404)
    return jsonify(specific_review.to_dict())


@app_views.route(
    '/reviews/<review_id>', methods=["DELETE"], strict_slashes=False)
def review_deleter(review_id):
    """ Deletes a specific Review object """
    specific_review = storage.get(Review, review_id)
    if specific_review is None:
        abort(404)
    storage.delete(specific_review)
    storage.save()
    return jsonify({}), 200


@app_views.route(
    '/places/<place_id>/reviews', methods=["POST"], strict_slashes=False)
def review_creator(place_id):
    """ Creates a new Review """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    request_data = request.get_json(silent=True)
    if request_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in request_data:
        abort(400, "Missing user_id")
    if "text" not in request_data:
        abort(400, "Missing text")
    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)
    request_data["place_id"] = place_id
    new_review = Review(**request_data)
    # storage.new(new_review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route(
    '/reviews/<review_id>', methods=["PUT"], strict_slashes=False)
def review_updater(review_id):
    """ Updates a specific Review object """
    specific_review = storage.get(Review, review_id)
    if specific_review is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in \
                ["id", "user_id", "place_id", "created_at", "updated_at"]:
            setattr(specific_review, key, value)
    storage.save()
    return jsonify(specific_review.to_dict()), 200
