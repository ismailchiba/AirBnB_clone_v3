#!/usr/bin/python3
"""
Contains class BaseModel
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from datetime import timezone, datetime
from sqlalchemy.ext.declarative import declarative_base
import uuid


if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if models.storage_t == 'db':
        id = Column(
            String(60),
            nullable=False,
            primary_key=True,
            unique=True)
        created_at = Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc))
        updated_at = Column(
            DateTime(timezone=True),
            nullable=False,
            default=datetime.now(timezone.utc))

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        time_format = '%Y-%m-%dT%H:%M:%S.%f%z'
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now(timezone.utc)
            self.updated_at = datetime.now(timezone.utc)

        else:
            for k, v in kwargs.items():
                if k == 'created_at' or k == 'updated_at':
                    # convert string values to formatted datetime objects
                    v = datetime.strptime(v, time_format)
                if k != '__class__':
                    # set all attributes except for class
                    setattr(self, k, v)
                if k == 'id':
                    setattr(self, k, v)
                if 'id' not in kwargs:
                    # supply id if missing
                    self.id = str(uuid.uuid4())
                if 'created_at' not in kwargs:
                    # supply created_at and updated_at if missing
                    self.created_at = datetime.now(timezone.utc)
                    self.updated_at = datetime.now(timezone.utc)

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict["created_at"] = new_dict["created_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
