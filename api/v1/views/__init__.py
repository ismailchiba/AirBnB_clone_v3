#!/usr/bin/python3
# api/v1/views/__init__.py

from flask import Blueprint

# Create a Blueprint with the prefix /api/v1
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import of the views (PEP8 may complain, but it's necessary)
from api.v1.views.index import *
