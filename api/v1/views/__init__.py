#!/usr/bin/python3
from flask import Blueprint

# package Ajouté 7. City
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
# For users
from api.v1.views.users import *
# 8. Amenity
from api.v1.views.amenities import *

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""
# package Ajouté 7. City
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
# For users
from api.v1.views.users import *
# 8. Amenity
from api.v1.views.amenities import *
"""
