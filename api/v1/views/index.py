#!/usr/bin/python3
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns a JSON response"""
    return {"status": "OK"}
