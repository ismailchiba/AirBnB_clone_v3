#!/usr/bin/python3
"""
initialize app_views
"""
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")
