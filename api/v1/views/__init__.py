from flask import Blueprint
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")
# adding status
from api.v1.views.index import *
