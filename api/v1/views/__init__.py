#!/usr/bin/python3
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
