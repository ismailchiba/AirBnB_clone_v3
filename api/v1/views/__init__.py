#!/usr/bin/python3
"""
<<<<<<< HEAD
views
=======
Created the flask blueprint
>>>>>>> storage_get_count
"""

from flask import Blueprint

<<<<<<< HEAD
#all the urls created with appviews must use the path /api/v1
app_views = Blueprint('app_views', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
#from api.v1.views.states import *
#from api.v1.views.amenities import *
#from api.v1.views.cities import *
#from api.v1.views.places import *
#from api.v1.views.places_reviews import *
#from api.v1.views.users import *
#from api.v1.views.places_amenities import *
=======
#all the urls we create must include /api/v1
app_views = Blueprint('app_views',__name__, url_prefix='/api/v1')

from api.v1.views.index import *
>>>>>>> storage_get_count
