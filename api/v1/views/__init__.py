#!/usr/bin/python3

"""initialization file for views module"""

from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

__all__ = ["amenities", "cities", "index", "places", "places_reviews", "states",
           "places_reviews1", "users", "app_views"]
# from index import *
# from states import *
# from cities import *
# from amenities import *
# from users import *
# from places import *
# from places_reviews import *
