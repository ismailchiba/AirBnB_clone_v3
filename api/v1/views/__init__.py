#!/usr/bin/python3

"""
Views for classes
"""

from flask import Blueprint

app_views = Blueprint('/api/v1', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
<<<<<<< HEAD
from api.v1.views.cities import *
from api.v1.views.users import *

=======
from api.v1.views.states import *
from api.v1.views.amenities import *
from api.v1.views.cities import *
from api.v1.views.places import *
from api.v1.views.places_reviews import *
from api.v1.views.places_amenities import *
from api.v1.views.users import *
>>>>>>> 6b6c4ec97ed5f0e046059b074222b06781a6eaf6
