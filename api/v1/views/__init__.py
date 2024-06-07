#!/usr/bin/python3
"""Runs everytime this module is invoked"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *

#app_views = Blueprint('app_views', __name__)
