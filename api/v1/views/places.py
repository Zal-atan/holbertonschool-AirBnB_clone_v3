#!/usr/bin/python3
""" User API calls module """

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.city import City
from models.user import User


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
    print("Getting Here 1")
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    print("Getting Here 2")
    # Checking to see if request data is a valid JSON
    # try:
    #     request_data = request.get_json()
    # except Exception as e:
    #     abort(400, f"Invalid JSON: {str(e)}")
    request_data = request.get_json(silent=True)
    print("Getting Here 3")
    if request_data is None:
        return abort(400, jsonify({"error": "Not a JSON"}))
    print("Getting Here 4")
    if "user_id" not in request_data:
        abort(400, jsonify({"error": "Missing user_id"}))
    print("Getting Here 5")
    # #  Check if user_id & name are present in request data
    # if not request_data or "user_id" not in request_data \
    #         or "name" not in request_data:
    #     abort(400, "Missing 'user_id' or 'name' in request data")

    user = storage.get(User, request_data["user_id"])
    if user is None:
        abort(404)
    print("Getting Here 6")
    if "name" not in request_data:
        abort(400, jsonify({"error": "Missing name"}))
    print("Getting Here 7")
    request_data["city_id"] = city_id
    print(request_data)
    new_place = Place(**request_data)
    # storage.new(new_place)
    storage.save()
    return make_response(jsonify(new_place.to_dict()), 201)


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
