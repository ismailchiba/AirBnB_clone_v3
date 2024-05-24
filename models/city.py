#!/usr/bin/python3
"""Defines the City class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class City(BaseModel, Base):
    """Represents a city in a geographic location system.

    This class inherits from BaseModel and links to the MySQL table 'cities'.
    It stores information about cities and their corresponding states.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store cities.
        name (sqlalchemy String): The name of the city.
        state_id (sqlalchemy String): The ID of the state the city belongs to.
        places (sqlalchemy relationship):
        Relationship with Place class to establish
        one-to-many association between cities and places.
    """

    __tablename__ = "cities"

    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship(
        "Place",
        backref="city",
        cascade="delete",
        passive_deletes=True
    )
