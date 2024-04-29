#!/usr/bin/python3
""" contain Database engine """

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """datastorage class"""
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """ interaacts with mysqk database"""
    __engine = None
    __session = None

    def __init__(self):
        """ creates engine """
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on current databasr"""
        _dict = {}
        if cls:
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                _dict[key] = item
            return _dict
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.CNC.get(class_name)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                _dict[key] = item
        return _dict

    def new(self, obj):
        """ adds objects to current database session """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        get spacitic obj"""
        _class = self.all(cls)

        for obj in _class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        count instance class"""
        return len(self.all(cls))

    def save(self):
        """ commits all changes of current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ delete ojects"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ reload1"""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """
            call remove()
        """
        self.__session.remove()
