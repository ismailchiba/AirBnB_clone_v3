#!/usr/bin/python3
""" Blueprint for API"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


from api.v1.views import app_views
from flask import jsonify

@app_views.route("/status")
def status():
    """
    returns OK status
    """
    return jsonify({"status": "OK"})
