#!/usr/bin/python3
"""
Package initializer for API v1 views.
"""

from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from api.v1.views.index import *  # noqa
from api.v1.views.states import *  # noqa
from api.v1.views.cities import *
from api.v1.views.amenities import *
