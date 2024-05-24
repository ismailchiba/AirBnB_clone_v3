#!/usr/bin/python3
"""Defines the BaseModel class."""
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

Base = declarative_base()


class BaseModel:
    """Defines the BaseModel class.

    Attributes:
        id (sqlalchemy String): The BaseModel's ID.
        created_at (sqlalchemy DateTime): The datetime of creation.
        updated_at (sqlalchemy DateTime): The datetime of last update.
    """

    id = Column(String(60), primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Initialize a new BaseModel instance.

        Args:
            *args (any): Unused.
            **kwargs (dict): Key/value pairs of attributes.
        """
        self.id = str(uuid4())
        self.created_at = self.updated_at = datetime.utcnow()
        if kwargs:
            for attr_name, attr_value in kwargs.items():
                if attr_name == "created_at" or attr_name == "updated_at":
                    attr_value = datetime.strptime(attr_value,
                                                   "%Y-%m-%dT%H:%M:%S.%f")
                if attr_name != "__class__":
                    setattr(self, attr_name, attr_value)

    def save(self):
        """Update the 'updated_at' attribute with the current datetime
        and save the instance."""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Return a dictionary representation of the BaseModel instance.

        Includes the key/value pair '__class__' representing
        the class name of the object.
        """
        instance_dict = self.__dict__.copy()
        instance_dict["__class__"] = str(type(self).__name__)
        instance_dict["created_at"] = self.created_at.isoformat()
        instance_dict["updated_at"] = self.updated_at.isoformat()
        instance_dict.pop("_sa_instance_state", None)
        return instance_dict

    def delete(self):
        """Delete the current instance from storage."""
        models.storage.delete(self)

    def __str__(self):
        """Return the string representation of the BaseModel instance."""
        instance_dict = self.__dict__.copy()
        instance_dict.pop("_sa_instance_state", None)
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, instance_dict)
