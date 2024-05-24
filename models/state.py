#!/usr/bin/python3
"""Defines the State class."""

import models
from os import getenv
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """Represents a state in a geographic location system.

    Inherits from BaseModel and links to the MySQL table 'states'.
    It stores information about states and their associated cities.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store states.
        name (sqlalchemy String): The name of the state.
        cities (sqlalchemy relationship):
        Relationship with City class to represent
            the cities within the state.
    """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="delete")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            """Get a list of all related City objects."""
            city_list = []
            for city in list(models.storage.all(City).values()):
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
