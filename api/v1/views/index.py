#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """returns a JSON: "status": "OK"."""
    return jsonify({"status": "OK"})
