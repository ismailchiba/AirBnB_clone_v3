#!/usr/bin/python3

"""
This is the state module.
It contains the State class that inherits from BaseModel.
It does the following:
- creates a relationship with the City class
- creates a backref for the state
- creates a getter attribute cities that returns the list of City instances
"""

import models
from models.base_model import BaseModel, Base
from models.city import City
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """
    This is the State class
    It defines the following attributes:
    - name: the state name
    - cities: the list of City instances with a state_id equal to the current State.id
    - It also creates a relationship with the City class
    Representation of state """
    if models.storage_t == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """
        This is the initialization of the State class
        It calls the super class with the following arguments:
        initializes state"""
        super().__init__(*args, **kwargs)

    if models.storage_t != "db":
        @property
        def cities(self):
            """
            This is the getter attribute cities that returns the list of City instances
            It returns the list of City instances with state_id equal to the current State.id
            getter for list of city instances related to the state"""
            city_list = []
            all_cities = models.storage.all(City)
            for city in all_cities.values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
