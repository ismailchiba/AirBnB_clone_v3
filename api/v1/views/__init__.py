#!/usr/bin/python3
""" initilize index module"""
from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import everything from api.v1.views.index
# PEP8 will complain about wildcard imports, but it's necessary in this case
from api.v1.views.index import *
from api.v1.views.states import *i
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
