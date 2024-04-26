#!/usr/bin/python3
"""return JSON """
from api.v1.views import app_views


@app_views.route('/status')
def status():
    stat = status = 'OK'}
    return stat
