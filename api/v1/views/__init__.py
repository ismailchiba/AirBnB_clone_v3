#!/usr/bin/python3

"""
This module initializes the blueprint object app_views
it does the following:
- imports the Blueprint class from the flask module
- creates a Blueprint object named app_views
- imports the modules containing the views
- registers the blueprint app_views
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
