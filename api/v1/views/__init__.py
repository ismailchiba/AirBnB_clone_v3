#!/usr/bin/python3
"""Blueprint for the API v1 views."""

from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Wildcard import (PEP8 warning expected, but we'll ignore it)
from .index import *
