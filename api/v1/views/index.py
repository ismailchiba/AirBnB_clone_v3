#!/usr/bin/python3
"""Import required module/lib"""
from api.v1.views import app_views


app_views = Blueprint()


@app_views.route('/status') 
