#!/usr/bin/python3
"""
create new flask app blueprint
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from ap.vi.views.index import *
