#!/usr/bin/python3
"""
City Class from Models Module
"""
import os
from models.base_model import BaseModel
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, Float, ForeignKey
import models

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

class City(BaseModel):
    """City class handles all application cities"""
    if storage_type == "db":
        __tablename__ = 'cities'
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship('Place', backref='cities', cascade='delete')
    else:
        def __init__(self, *args, **kwargs):
            """Instantiation of new City class."""
            super().__init__(*args, **kwargs)
            self.state_id = ''
            self.name = ''

        @property
        def places(self):
            """
            Getter for places
            :return: list of places in that city
            """
            all_places = models.storage.all("Place")

            result = []

            for obj in all_places.values():
                if str(obj.city_id) == str(self.id):
                    result.append(obj)

            return result
