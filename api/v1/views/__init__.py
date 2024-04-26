#!/usr/bin/python3
"""Status of your API"""

from .index import *
from flask import Blueprint
from api.v1.views import amenities
from api.v1.views import cities
from api.v1.views import states


app_views = Blueprint('app_views', __name__, url='/api/v1')
