#!/usr/bin/python3
""" Database engine for storing class instances in a MySQL database """

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """ Handles long-term storage of all class instances """

    # Class Name to Class Mapping (for database operations)
    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    def __init__(self):
        """ Initializes the database engine """
        # Create database engine using environment variables
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))

        # Drop all tables if running in test environment
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Retrieves all objects from the database """
        obj_dict = {}

        if cls:
            # Query objects of a specific class
            obj_class = self.__session.query(self.CNC.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
            return obj_dict

        # Query objects of all classes
        for class_name in self.CNC:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(self.CNC.get(class_name)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """ Adds a new object to the current database session """
        self.__session.add(obj)

    def get(self, cls, id):
        """ Retrieves a specific object from the database """
        all_class = self.all(cls)
        for obj in all_class.values():
            if id == str(obj.id):
                return obj
        return None

    def count(self, cls=None):
        """ Counts the number of instances of a class """
        return len(self.all(cls))

    def save(self):
        """ Commits all changes in the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes an object from the current database session """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all database tables & initializes new database session """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
            )
        )

    def close(self):
        """ Closes the database session """
        self.__session.remove()
