#!/usr/bin/python3
"""
Review Class from Models Module
"""
import os
from models.base_model import BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey

storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class Review(BaseModel):
    """Review class handles all application reviews"""
    if storage_type == "db":
        __tablename__ = 'reviews'
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    else:
        def __init__(self, *args, **kwargs):
            """Instantiation of new Review class."""
            super().__init__(*args, **kwargs)
            self.text = ''
            self.place_id = ''
            self.user_id = ''
