#!/usr/bin/python3
from flask import Blueprint
# package Ajouté 7. City
from api.v1.views.states import *
from api.v1.views.cities import *
# 8. Amenity
from api.v1.views.amenities import *
# 9. User
from api.v1.views.users import *


app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
"""
# package Ajouté 7. City
from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
# 8. Amenity
from api.v1.views.amenities import *
# 9. User
<<<<<<< HEAD
from api.v1.views.users import *
"""
=======
# from api.v1.views.users import *
>>>>>>> 5f97592faa1c2804df68a28fdd8e5649e85e7842
