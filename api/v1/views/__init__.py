#!/usr/bin/python3

"""creates the app_views Blueprint here"""


from flask import Blueprint as B

app_views = B('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
