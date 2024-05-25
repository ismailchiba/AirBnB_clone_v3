#!/usr/bin/python3
"""Blueprint instance"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

city_views = Blueprint("city_views", __name__, url_prefix="/api/v1")


class Views:
    """TO stop importation Error"""
    from api.v1.views.index import get_status
