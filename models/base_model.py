#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4, UUID
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime


storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class BaseModel:
    """
    Attributes and functions for BaseModel class.
    """
    if storage_type == 'db':
        # Define database columns if using SQLAlchemy
        pass

    def __init__(self, *args, **kwargs):
        """Instantiation of new BaseModel class."""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
        # Ensure that updated_at is set when initializing from kwargs
        self.updated_at = kwargs.get('updated_at', self.created_at)

    def bm_update(self, name, value):
        """
        Update the basemodel and sets the correct attributes.
        """
        setattr(self, name, value)
        if self.storage_type != 'db':
            self.save()

    def save(self):
        """Update attribute updated_at to current time."""
        if storage_type != 'db':
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """ Return a dictionary representation of BaseModel """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary

    def to_json(self):
        """returns json representation of self"""
        bm_dict = self.to_dict()  # Reuse the existing to_dict method
        for key, value in bm_dict.items():
            if isinstance(value, datetime):
                bm_dict[key] = value.isoformat()  # Convert datetime objects to ISO format
        return bm_dict


    def __str__(self):
        """returns string type representation of object instance"""
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
            deletes current instance from storage
        """
        self.delete()

    def __is_serializable(self, value):
        """Checks if a value is serializable."""
        try:
            json.dumps(value)
            return True
        except TypeError:
            return False
