#!/usr/bin/python3
"""Module for the index of blueprint"""

from api.v1.views import app_views
from flask import jsonify


# creating a route /status on the object app_views that returns a JSON
@app_views.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "OK"}), 200
