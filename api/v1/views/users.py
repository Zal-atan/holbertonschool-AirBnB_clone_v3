#!/usr/bin/python3
""" User API calls module """

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.user import User


@app_views.route('/users', methods=["GET"], strict_slashes=False)
def user_getter():
    """ List all User objects """
    list_users = [user.to_dict() for user in storage.all(
        User).values()]
    return jsonify(list_users)


@app_views.route(
        '/users/<user_id>', methods=["GET"], strict_slashes=False)
def specific_user_getter(user_id):
    """ Retrieves data oof a specific User from ID """
    specific_user = storage.get(User, user_id)
    if specific_user is None:
        abort(404)
    return jsonify(specific_user.to_dict())


@app_views.route(
        '/users/<user_id>', methods=["DELETE"], strict_slashes=False)
def user_deleter(user_id):
    """ Deletes a specific User object """
    specific_user = storage.get(User, user_id)
    if specific_user is None:
        abort(404)
    storage.delete(specific_user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=["POST"], strict_slashes=False)
def user_creator():
    """ Creates a new User """
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    if "email" not in request_data:
        abort(400, "Missing email")
    if "password" not in request_data:
        abort(400, "Missing password")
    new_user = User(**request_data)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route(
        '/users/<user_id>', methods=["PUT"], strict_slashes=False)
def user_updater(user_id):
    """ Updates a specific User object """
    specific_user = storage.get(User, user_id)
    if specific_user is None:
        abort(404)
    request_data = request.get_json()
    if request_data is None:
        abort(400, "Not a JSON")
    for key, value in request_data.items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(specific_user, key, value)
    storage.save()
    return jsonify(specific_user.to_dict()), 200
