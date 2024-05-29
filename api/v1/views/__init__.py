#!/usr/bin/python3
"""Defines the API version 1 blueprint for Flask applications.

This blueprint groups together URL routes for various functionalities
related to places, amenities, users, and more. It provides a structured
way to organize and manage API endpoints within your Flask application.
"""
from flask import Blueprint
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.index import *
from api.v1.views.places_amenities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.states import *
from api.v1.views.users import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
