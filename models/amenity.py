#!/usr/bin/python

"""
This is the amenity module.
it contains the Amenity class that inherits from BaseModel
it does the following:
- creates a relationship with the Place class
- creates a backref for amenities
- creates a getter attribute place_amenities that returns the list of Place instances
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """
    This is the Amenity class
    Representation of Amenity 
    """
    if models.storage_t == 'db':
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        This is the initialization of the Amenity class
        initializes Amenity
        """
        super().__init__(*args, **kwargs)
