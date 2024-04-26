#!/usr/bin/python3
"""
    index module
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route("/status", methods=['GET'], strict_slashes=False)
def status():
    """send a 200 reponse to cliet with format 'status': 'ok'"""
    return jsonify(status="OK")
