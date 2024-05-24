#!/usr/bin/python3
"""Defines the Place class."""

import models
from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import Column, Float, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship


association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True, nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True, nullable=False))


class Place(BaseModel, Base):
    """Represents a place in a lodging system.

    Inherits from BaseModel and links to the MySQL table 'places'.
    It stores information about lodging places, such as their location,
    amenities, and user ratings.

    Attributes:
        __tablename__ (str):
        The name of the MySQL table to store places.
        city_id (sqlalchemy String):
        The ID of the city where the place is located.
        user_id (sqlalchemy String):
        The ID of the user who owns the place.
        name (sqlalchemy String):
        The name of the place.
        description (sqlalchemy String):
        The description of the place.
        number_rooms (sqlalchemy Integer):
        The number of rooms in the place.
        number_bathrooms (sqlalchemy Integer):
        The number of bathrooms in the place.
        max_guest (sqlalchemy Integer):
        The maximum number of guests the place can accommodate.
        price_by_night (sqlalchemy Integer):
        The price per night for the place.
        latitude (sqlalchemy Float):
        The latitude coordinate of the place.
        longitude (sqlalchemy Float):
        The longitude coordinate of the place.
        reviews (sqlalchemy relationship):
        Relationship with Review class to represent
            the reviews associated with the place.
        amenities (sqlalchemy relationship):
        Relationship with Amenity class to represent
            the amenities available in the place.
        amenity_ids (list):
        A list of IDs of linked amenities.
    """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0)
    number_bathrooms = Column(Integer, default=0)
    max_guest = Column(Integer, default=0)
    price_by_night = Column(Integer, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Get a list of all linked reviews."""
            review_list = []
            for review in list(models.storage.all(Review).values()):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Get/set linked amenities."""
            amenity_list = []
            for amenity in list(models.storage.all(Amenity).values()):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if isinstance(value, Amenity):
                self.amenity_ids.append(value.id)
