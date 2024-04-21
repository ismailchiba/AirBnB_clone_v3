#!/usr/bin/python3

"""Module for API views"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
""" Blueprint object that handles all views for API v1"""


from api.v1.views.index import *
""" Importing index module for the API"""


from api.v1.views.users import *
""" Importing users module for the API"""


from api.v1.views.places_reviews import *
""" Importing places module for the API"""

from api.v1.views.places import *
""" Importing places module for the API"""

from api.v1.views.states import *
""" Importing states module for the API"""

