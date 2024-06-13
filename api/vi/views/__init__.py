from flask import Blueprint

# Create a Blueprint instance with url prefix /api/v1
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

# Import views from index.py to avoid circular import
from api.v1.views.index import *
