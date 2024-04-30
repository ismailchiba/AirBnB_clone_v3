#!/usr/bin/python3
"""Routes are defined here."""
from api.v1.views import app_views
import json


@app_views.route('/status')
def status():
    """returns OK status."""
    stat = {
        "status": "OK"
    }
    return (json.dumps(stat, indent=2) + '\n')
