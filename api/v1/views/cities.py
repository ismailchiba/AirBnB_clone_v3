#!/usr/bin/python3
"""
API version 1 views
"""
from api.v1.views import app_views
from flask import jsonify, request
from models import storage
from models.city import City
from api.v1.views.custom import appendRoutes


appendRoutes(City, "cities")
