#!/usr/bin/python3
""" User API calls module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User
from models.city import City
from models.place import Place


@app_views.route(
        '/cities/<city_id>/places', methods=["GET"], strict_slashes=False)
def places_getter(city_id):
    """ List all Place objects of a City """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    list_places = [place.to_dict() for place in city.places]
    return jsonify(list_places)


@app_views.route(
        '/places/<place_id>', methods=["GET"], strict_slashes=False)
def specific_place_getter(place_id):
    """ Retrieves data of a specific Place from ID """
    specific_place = storage.get(Place, place_id)
    if specific_place is None:
        abort(404)
    return jsonify(specific_place.to_dict())


@app_views.route(
        '/places/<place_id>', methods=["DELETE"], strict_slashes=False)
def place_deleter(place_id):
    """ Deletes a specific Place object """
    specific_place = storage.get(Place, place_id)
    if specific_place is None:
        abort(404)
    storage.delete(specific_place)
    storage.save()
    return jsonify({}), 200


@app_views.route(
        '/cities/<city_id>/places', methods=["POST"], strict_slashes=False)
def place_creator(city_id):
    """ Creates a new Place """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    if "user_id" not in request_data:
        abort(400, "Missing user_id")
    if "name" not in request_data:
        abort(400, "Missing name")
    user = storage.get(User, request_data["user.id"])
    if user is None:
        abort(404)
    new_place = Place(
        city_id=city_id, user_id=request_data["user_id"], **request_data)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route(
        '/places/<place_id>', methods=["PUT"], strict_slashes=False)
def place_updater(place_id):
    """ Updates a specific Place object """
    specific_place = storage.get(Place, place_id)
    if specific_place is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(specific_place, key, value)
    storage.save()
    return jsonify(specific_place.to_dict()), 200
