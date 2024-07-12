#!/usr/bin/python3
"""Returns Json"""
from api.v1.views import app_views
import json

@app_views.route('/status')
def status():
    return json.dumps({"status": "OK"})