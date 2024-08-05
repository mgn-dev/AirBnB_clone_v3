#!/usr/bin/python3
"""Module that models index page routes."""

from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['GET'])
def get_status():
    """Returns the api's status."""
    return jsonify({"status": "OK"})
