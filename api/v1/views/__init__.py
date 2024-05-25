#!/usr/bin/python3
"""Blueprint instance"""
from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")


class Views:
    """TO stop importation Error"""
    from api.v1.views.index import get_status, get_stats
    from api.v1.views.states import state, one_state, del_state, post_state, update_state
    from api.v1.views.amenities import get_amenities, one_amenity, remove_amenity, create_amenity, update_amenity
    from api.v1.views.places import get_places, get_place, delete_place, create_place
