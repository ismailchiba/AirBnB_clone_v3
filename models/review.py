#!/usr/bin/python3
"""Defines the Review class."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey


class Review(BaseModel, Base):
    """Represents a review in a lodging system.

    Inherits from BaseModel and links to the MySQL table 'reviews'.
    It stores information about reviews for lodging places.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store reviews.
        text (sqlalchemy String): The content of the review.
        place_id (sqlalchemy String): The ID of the place being reviewed.
        user_id (sqlalchemy String): The ID of the user who wrote the review.
    """

    __tablename__ = "reviews"

    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
