#!/usr/bin/python3
""" Creates a /status route"""

from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status")
def status_page():
    """Page declaring 'status': OK"""
    return jsonify({"status": "OK"})
