#!/usr/bin/python3
<<<<<<< HEAD
"""It initializes the package 'views'."""

from flask import Blueprint
from api.v1.views.index import *
from api.v1.views import cities.py
from api.v1.views import users.py
from api.v1.views import places_reviews.py
from api.v1.views import places_amenities.py

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

    def __init__(self):
        """An empty method"""
        pass
=======
"""
Views for AirBnB_clone_v3
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
>>>>>>> dff4a60a4ac807bc9108c52bf6cb81f811eec8a5
