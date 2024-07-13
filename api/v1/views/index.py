#!/usr/bin/python3
""" Defines a status route """
from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """
    returns OK status
    """
    return jsonify({"status": "OK"})
