#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None
    __models = {}

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')

        self.__models = {"Amenity": Amenity, "City": City,
                         "Place": Place, "Review": Review,
                         "State": State, "User": User}

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in self.__models:
            if cls is None or cls is self.__models[clss] or cls is clss:
                objs = self.__session.query(self.__models[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

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
        sess_factory = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieve an object from the database based on its class type and ID.

        Args:
            cls (type): The class type of the object to retrieve.
            id (str): The unique identifier of the object.

        Returns:
            object: The object matching the class and ID, or None if no such
            object exists.
        """
        if not id or not cls:
            return None
        if isinstance(cls, str):
            for key in self.__models.keys():
                if key == cls:
                    cls = self.__models[key]
        if cls not in self.__models.values():
            return None

        return self.__session.query(cls).filter(cls.id == id).one_or_none()

    def count(self, cls=None):
        """
        Retrieve the number of objects in the database of a specific class
        or for all classes.

        Args:
            cls (type, optional): The class type of the objects to count.
            Defaults to None.

        Returns:
            int: The number of objects of the specified class in the database.
            If cls is None, returns the total number of objects in all classes.
        """
        return len(self.all(cls))
