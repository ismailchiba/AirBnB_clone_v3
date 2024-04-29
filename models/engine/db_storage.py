#!/usr/bin/python3

"""This module is used to interact with the MySQL database
Contains the class DBStorage
And the dictionary classes
It will be imported in the __init__.py module
"""

from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """This class will be used to interact with the MySQL database
    It will be used to store and retrieve objects from the database
    interacts with the MySQL database
    """
    __engine = None
    __session = None

    def __init__(self):
        """This creates an instance of the DBStorage class
        Instantiate a DBStorage object
        And creates the engine and session attributes
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """This method returns a dictionary of objects
        It returns a dictionary of objects of the class name passed
        query on the current database session
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """This will add the object to the current database session
        add the object to the current database session
        It will add the object to the current database session
        """
        self.__session.add(obj)

    def save(self):
        """This will commit all changes of the current database session
        commit all changes of the current database session
        It will commit all changes of the current database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """This will delete from the current database session
        delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """This will reload data from the database
        reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        This will retrieve an object based on the class name and its ID
        It then returns the object based on the class name and its ID
        Returns the object based on the class name and its ID, or None if not
        found
        """
        if cls in classes.values():
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def count(self, cls=None):
        """This will return the number of objects in storage
        And the number of objects in storage matching the class name
        Returns the number of objects in storage matching the given class name.
        If no name is passed, returns the count of all objects in storage.
        """
        return len(self.all(cls))
