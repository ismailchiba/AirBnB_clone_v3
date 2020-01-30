#!/usr/bin/python3
""" import Blueprint and create instance Blueprint """


from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from models.state import state


from api.v1.views.index import *
from api.v1.views.states import *
