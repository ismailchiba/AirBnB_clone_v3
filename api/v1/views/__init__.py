from flask import Blueprint

# Create a Blueprint instance
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Wildcard import everything from api.v1.views.index
# PEP8 will complain about wildcard imports, but it's necessary in this case
from api.v1.views.index import *
