#!/usr/bin/python3
""" A module that initialises the views model with a blueprint app_views"""
from flask import Blueprint
from index import *


app_views = Blueprint('/api/vi', __name__, url_prefix='/api/v1')
