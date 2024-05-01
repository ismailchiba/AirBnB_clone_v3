#!/usr/bin/python3
"""Return status of API."""
from api.v1.views import app_views


@app_views.route('/status')
def appviews():
    """Get status of API."""
    return {
        "status": "OK",
    }
