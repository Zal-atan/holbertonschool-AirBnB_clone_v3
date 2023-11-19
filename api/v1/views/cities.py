#!/usr/bin/python3
""" City API Calls module"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.state import City


@app_views.route('/states/<state_id>/cities', methods=["GET"], strict_slashes=False)
def cities_getter(state_id):
    """ Retrieves the list of all City objects of a State """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=["GET"], strict_slashes=False)
def specific_city_getter(city_id):
    """ Retrieves a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=["DELETE"], strict_slashes=False)
def city_deleter(city_id):
    """ Deletes a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=["POST"], strict_slashes=False)
def city_creator(state_id):
    """ Creates a City """
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    if "name not in request_data":
        abort(400, "Missing name")

    new_city = City(**request_data)
    new_city.state_id = state_id
    new_city.save()

    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=["PUT"], strict_slashes=False)
def city_updater(city_id):
    """ Updates a City object """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")

    # Update the City objects w/ all KVP of the dictionary
    for key, value in request_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(city, key, value)

    city.save()

    return jsonify(City.to_dict()), 200
