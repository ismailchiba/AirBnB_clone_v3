#!/usr/bin/python3
""" Starts the Blueprint views """
from flask import Blueprint

# Create a blueprint named 'app_views' with URL prefix '/api/v1'
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
