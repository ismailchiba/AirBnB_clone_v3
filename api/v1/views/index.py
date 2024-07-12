#!/usr/bin/python3
"""Returns Json"""
from api.v1.views import app_views
import json

@app_views.route('/status')
def status():
    status = json.dumps({"status": "OK"})
    return status, 200