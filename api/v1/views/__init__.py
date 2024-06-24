#!/usr/bin/python3
"""
views
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
app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.users import *
from api.v1.views.places_amenities import *
>>>>>>> 8471f4eadde8806234297f3b75e7ad8d245a4f73
