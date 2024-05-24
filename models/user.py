#!/usr/bin/python3
"""Defines the User class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents a user in a lodging system.

    Inherits from BaseModel and links to the MySQL table 'users'.
    It stores information about users, including their personal details,
    places they own, and reviews they've written.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store users.
        email (sqlalchemy String): The email address of the user.
        password (sqlalchemy String): The password of the user.
        first_name (sqlalchemy String): The first name of the user.
        last_name (sqlalchemy String): The last name of the user.
        places (sqlalchemy relationship):
        Relationship with Place class to represent
            the places owned by the user.
        reviews (sqlalchemy relationship):
        Relationship with Review class to represent
            the reviews written by the user.
    """

    __tablename__ = "users"

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    places = relationship("Place", backref="user", cascade="delete")
    reviews = relationship("Review", backref="user", cascade="delete")
