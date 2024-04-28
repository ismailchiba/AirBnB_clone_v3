#!/usr/bin/python3
'''let's configure flask status'''
from flask import jsonify
from api.v1.views import app_views
import models
from models.base_model import BaseModel


@app_views.route('/status', strict_slashes=False)
def status():
    ''' shows the status'''
    return jsonify(status='OK')
