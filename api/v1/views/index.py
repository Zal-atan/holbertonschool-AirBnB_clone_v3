#!/usr/bin/python3
""" Creates a /status route"""

from api.v1.views import app_views


@app_views.route("/status")
def status_page():
    """Page declaring 'status': OK"""
    return {"status": "OK"}.json()
