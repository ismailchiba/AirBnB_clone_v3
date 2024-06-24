#!/usr/bin/python3
"""
Amenity Class from Models Module
"""
import os
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float

storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class Amenity(BaseModel):
    """Amenity class handles all application amenities"""
    if storage_type == "db":
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity")
    else:
        def __init__(self, *args, **kwargs):
            """Instantiation of new Amenity class."""
            super().__init__(*args, **kwargs)
            self.name = ''

    def to_dict(self):
        """Returns a dictionary representation of the Amenity instance"""
        amn_dict = self.__dict__.copy()
        amn_dict.pop('_sa_instance_state', None)
        return amn_dict
