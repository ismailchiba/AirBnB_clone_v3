#!/usr/bin/python3

from flask import Blueprint
from api.v1.views.index import *

# Creating an instance of Blueprint with URL prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Importing everything in the package of api.v1.views.index
# pylint: disable=wildcard-import
