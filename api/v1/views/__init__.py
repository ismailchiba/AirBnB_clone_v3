#!/usr/bin/python3
"""
This init.py will import the bluprint of our app
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
