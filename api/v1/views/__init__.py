#!/usr/bin/python3
"""Status of your API"""

from .index import *
from flask import Blueprint


app_views = Blueprint('app_views', __name__, url='/api/v1')
