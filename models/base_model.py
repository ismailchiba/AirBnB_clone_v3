#!/usr/bin/python3
"""
BaseModel Class of Models Module
"""

import os
import json
import models
from uuid import uuid4
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime

storage_type = os.environ.get('HBNB_TYPE_STORAGE')

"""
    Creates instance of Base if storage type is a database
    If not database storage, uses class Base
"""
if storage_type == 'db':
    Base = declarative_base()
else:
    class Base:
        pass


class BaseModel:
    """
    BaseModel Class for the Models Module
    """

    if storage_type == 'db':
        id = Column(String(60), nullable=False, primary_key=True)
        created_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())
        updated_at = Column(DateTime, nullable=False,
                            default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiation of a new BaseModel instance"""
        self.id = str(uuid4())
        self.created_at = datetime.now()
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)

    def __is_serializable(self, obj_v):
        """
        Private method to check if an object is serializable
        """
        try:
            obj_to_str = json.dumps(obj_v)
            return obj_to_str is not None and isinstance(obj_to_str, str)
        except Exception:
            return False

    def bm_update(self, name, value):
        """
        Update the basemodel and sets the correct attributes
        """
        setattr(self, name, value)
        if storage_type != 'db':
            self.save()

    def save(self):
        """
        Update the updated_at attribute to the current time
        """
        if storage_type != 'db':
            self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_json(self):
        """
        Return JSON representation of self
        """
        bm_dict = {}
        for key, value in self.__dict__.items():
            if self.__is_serializable(value):
                bm_dict[key] = value
            else:
                bm_dict[key] = str(value)
        bm_dict['__class__'] = type(self).__name__
        if '_sa_instance_state' in bm_dict:
            bm_dict.pop('_sa_instance_state')
        if storage_type == "db" and 'password' in bm_dict:
            bm_dict.pop('password')
        return bm_dict

    def __str__(self):
        """
        Return string type representation of object instance
        """
        class_name = type(self).__name__
        return '[{}] ({}) {}'.format(class_name, self.id, self.__dict__)

    def delete(self):
        """
        Delete current instance from storage
        """
        self.delete()
