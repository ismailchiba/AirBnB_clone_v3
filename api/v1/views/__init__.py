#!/usr/bin/python3
"""
This module initializes the blueprint for the views and imports the routes.
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index
