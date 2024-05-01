#!/usr/bin/python3
""" holds class User"""
import hashlib
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user."""

    if models.storage_t == "db":
        __tablename__ = "users"
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if kwargs:
            __password = kwargs.pop('password', None)
            if __password:
                User.__password = ""
                hashed_pwd = self._hash_password()
                setattr(self, "password", hashed_pwd)
        super().__init__(*args, **kwargs)
        # Ensure that the password is hashed upon object creation

    def _hash_password(self):
        """Hashes the user's password using md5."""
        return hashlib.md5(self.__password.encode('utf-8')).hexdigest()

    @property
    def hashed_pwd(self):
        """Returns the hashed password."""
        return self.__password
