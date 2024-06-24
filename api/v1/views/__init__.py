#!/usr/bin/python3
from flask import Blueprint

# Create a blueprint instance with url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import specific modules
from api.v1.views.index import *
from api.v1.views.states import *
