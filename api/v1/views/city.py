#!/usr/bin/python3
""" City API Calls module"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route("/states/<state_id>/cities", methods=["GET"],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Gets all City objects from a given state of id <state_id>: returns
    as a json. 404 Error if incorrect state"""
    specific_state = storage.get(State, state_id)
    if specific_state is None:
        abort(404)
    list_cities = [city.to_dict() for city in storage.all(
        City).values() if city.state_id == state_id]
    return jsonify(list_cities)

@app_views.route("/cities/<city_id>", methods=["GET"],
                 strict_slashes=False)
def get_specific_city(city_id):
    """Takes a specific city id and returns the json information of that city
    object. 404 Error if not found"""
    specific_city = storage.get(City, city_id)
    if specific_city is None:
        abort(404)
    return jsonify(specific_city.to_dict())
