#!/usr/bin/python3
'''
create the app
'''
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='api/v1/')

from app.v1.views.index import *
