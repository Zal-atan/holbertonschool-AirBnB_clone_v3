#!/usr/bin/python3
""" States API Calls module"""

from api.v1.views import app_views
from flask import jsonify, abort
from models import storage
from models.state import State


@app_views.route('/states', methods=["GET"], strict_slashes=False)
def state_getter():
    """ List all of objects of class State """
    list_states = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(list_states)


@app_views.route('/states/<id>', methods=["GET"], strict_slashes=False)
def specific_state_getter(id):
    """Retrieves the data of a specific state from the given ID"""
    specific_state = storage.get(State, id)
    if specific_state is None:
        abort(404)
    return jsonify(specific_state.to_dict())
