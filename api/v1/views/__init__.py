#!/usr/bin/python3
"""
Create flask app bluie print
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_profile='/api/v1')

from api.v1.views.index import *
