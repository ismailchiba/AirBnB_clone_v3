#!/usr/bin/python3
'''index for blueprint'''

from api.v1.views import app_views

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    '''returns status'''
    return {"status": "OK"}
