#!/usr/bin/python3

from api.v1.views import app_views
from flask import jsonify


@app_view.rout('/status', method=['GET'])
def status():
    return jsonify({"status": "OK"})
