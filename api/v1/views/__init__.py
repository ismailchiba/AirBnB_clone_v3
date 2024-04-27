from flask import Blueprint

# Create the Blueprint instance with the URL prefix
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
from .index import *
