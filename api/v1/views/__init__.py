#!/usr/bin/python3
# Un comentario

from flask import Blueprint

app_views = Blueprint('index', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
