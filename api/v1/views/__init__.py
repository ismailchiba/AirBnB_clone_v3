#!/usr/bin/python3
from flask import Blueprint
""" this area is for file description"""


app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
from api.v1.views.index import *
