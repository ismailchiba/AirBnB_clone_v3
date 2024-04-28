#!/usr/bin/python3
""" Module for status"""
from api.v1.views import app_views


@app_views.route("/status", strict_slashes=False)
def status():
    """returns status"""
    return {"status": "OK"}
