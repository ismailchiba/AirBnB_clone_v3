#!/usr/bin/python3
"""That module will define a blueprint for a routes with Blueprint object"""
from flask import Blueprint


app_views = Blueprint("app_views", __name__, url_prefix='/api/v1')

from api.v1.views.index import *
