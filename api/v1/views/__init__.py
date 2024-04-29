#!/usr/bin/python3

"""
This module will or is a blueprint object that handles all views for the application
create a blueprint object that handles all views for the application
It will be imported in the app.py module
"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')


from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
from api.v1.views.index import *
from api.v1.views.states import *
