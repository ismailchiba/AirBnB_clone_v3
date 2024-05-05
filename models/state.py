#!/usr/bin/python3
""" holds class State"""
import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", cascade="all, delete-orphan", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """Getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list

    def to_dict(self):
        """Returns a dictionary representation of the State instance"""
        state_dict = {
            "__class__": type(self).__name__,
            "id": self.id,
            "created_at": self.created_at.isoformat() if hasattr(self, 'created_at') else None,
            "updated_at": self.updated_at.isoformat() if hasattr(self, 'updated_at') else None,
            "name": self.name
            
        }
        return state_dict
