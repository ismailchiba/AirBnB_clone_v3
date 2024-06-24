#!/usr/bin/python3
"""Blueprints intialization of APIs"""

from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


# wildcard importing of everything in the api.v1.views.index package
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
