#!/usr/bin/python3
"""
Creat Flask app; connect index.py to API
"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage



@app_views.route('/status', strict_slashes=False)
def hbnb_status():
    """hbnb Status"""
    return jsonify({"status": "OK"})
