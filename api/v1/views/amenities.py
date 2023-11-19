#!/usr/bin/python3
""" Amenity API calls module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def amenity_getter():
    """ List all Amenity objects """
    list_amenities = [amenity.to_dict() for amenity in storage.all(
        Amenity).values()]
    return jsonify(list_amenities)


@app_views.route(
        '/amenities/<amenity_id>', methods=["GET"], strict_slashes=False)
def specific_amenity_getter(amenity_id):
    """ Retrieves data oof a specific AAmenity from ID """
    specific_amenity = storage.get(Amenity, amenity_id)
    if specific_amenity is None:
        abort(404)
    return jsonify(specific_amenity.to_dict())


@app_views.route(
        '/amenities/<amenity_id>', methods=["DELETE"], strict_slashes=False)
def amenity_deleter(amenity_id):
    """ Deletes a specific AAmenity object """
    specific_amenity = storage.get(Amenity, amenity_id)
    if specific_amenity is None:
        abort(404)
    storage.delete(specific_amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def amenity_creator():
    """ Creates a new Amenity """
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    if "name" not in request_data:
        abort(400, "Missing name")
    new_amenity = Amenity(**request_data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route(
        '/amenities/<amenity_id>', methods=["PUT"], strict_slashes=False)
def amenity_updates(amenity_id):
    """ Updates a specific Amenity object """
    specific_amenity = storage.get(Amenity, amenity_id)
    if specific_amenity is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(specific_amenity, key, value)
    storage.save()
    return jsonify(specific_amenity.to_dict()), 200
