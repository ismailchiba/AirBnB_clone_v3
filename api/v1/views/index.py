#!/usr/bin/python3
""" index routes """
from api.v1.views import app_views
from flask import jsonify


@app_views.route("/status")
def get_status():
    """Status of my API"""
    return jsonify({"status": "OK"})
