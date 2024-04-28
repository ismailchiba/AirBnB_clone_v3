#!/usr/bin/python3
"""
Created the flask blueprint
"""

from flask import Blueprint

#all the urls we create must include /api/v1
app_views = Blueprint('app_views',__name__, url_prefix='/api/v1')

from api.v1.views.index import *