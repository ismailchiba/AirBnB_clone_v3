#!/usr/bin/python3
"""
Blueprint for API
"""
if __name__ == "__main__":
    import api.v1.views.index
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
