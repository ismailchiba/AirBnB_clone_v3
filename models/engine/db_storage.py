#!/usr/bin/python3
"""Contains the class DBStorage"""

import models
import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """handles long term storage of all class instances"""
    Classmap = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """interact with MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """ creates the engine self.__engine """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ returns a dictionary of all objects """
        obj_dict = {}
        if cls:
            obj_classes = self.__session.query(self.Classmap.get(cls)).all()
            for item in obj_classes:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
            return obj_dict
        for class_names in self.Classmap:
            if class_names == 'BaseModel':
                continue
            obj_classes = self.__session.query(
                self.Classmap.get(class_names)).all()
            for item in obj_classes:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
        return (obj_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def get(self, cls, id):
        """method to retrieve one object"""
        all_class = self.all(cls)
        """ilterate over each object"""
        for obj in all_class.values():
            if id == str(obj.id):
                return (obj)
        """if no matching object is found return none"""
        return (None)

    def count(self, cls=None):
        """count number of object in storage"""
        return len(self.all(cls))

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))


    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
