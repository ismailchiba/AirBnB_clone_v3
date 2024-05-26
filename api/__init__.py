#!/usr/bin/python3
"""
Initialization of the views package
"""

from flask import Blueprint

# Import all view modules to register their routes with the blueprint
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *

# Create a Blueprint for the API v1
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
