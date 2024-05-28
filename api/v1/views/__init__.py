#!/usr/bin/python3
"""
<<<<<<< HEAD
views for AirBnB_clone_v3
=======
Views for AirBnB_clone_v3
>>>>>>> 76e9b7a83b6178fbb7b20d3026cfb7422a70b8a3
"""

from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
from api.v1.views.users import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
