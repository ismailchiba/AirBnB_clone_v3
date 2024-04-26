#!/usr/bin/python3
"""create a blueprint"""

from flask import Blueprint
from api.v1.views.index import *


app_views = Blueprint(app_views)
@app_views.route('/api/v1')
