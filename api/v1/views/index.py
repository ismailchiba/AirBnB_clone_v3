#!/usr/bin/python3
"""Index file of the views module
"""
from api.v1.views import app_views


@app_views.route('/status')
def getStatus():
    """function to return status of response
    """
    resp = {"status": "OK"}
    return resp
