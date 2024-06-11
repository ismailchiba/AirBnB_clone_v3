#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import os
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
from sqlalchemy.ext.declarative import declarative_base

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiating a DBStorage object"""
        try:
            import MySQLdb
            print("MySQLdb is installed successfully!")
        except ImportError as e:
            print("MySQLdb is not installed: {e}")
            
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        
        print("HBNB_MYSQL_USER: {}".format(HBNB_MYSQL_USER))
        print("HBNB_MYSQL_PWD: {}".format(HBNB_MYSQL_PWD))
        print("HBNB_MYSQL_HOST: {}".format(HBNB_MYSQL_HOST))
        print("HBNB_MYSQL_DB: {}".format(HBNB_MYSQL_DB))
        
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        
        print("engine created successfully!")
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
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
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        retrieves all objects in storage
        Args:
            cls (class): The class of the object to retrieve.
            id (str): The ID of the object to retrieve.
        Return:
            object: The object instance if found, otherwise None.
        """
        all_objs = self.all()
        for key, values in all_objs.items():
            if key.split('.')[1] == id:
                return values
        return None

    def count(self, cls=None):
        """
        Counts the number of objects in storage.
        Args:
            cls (class, optional): The class of objects to count.
            If None, counts all objects.
        Returns:
            number of objects in storage matching the given class.
            else count of all objects in storage
        """
        classes = {
            "Amenity": Amenity,
            "City": City,
            "Place": Place,
            "Review": Review,
            "State": State,
            "User": User
              
        }
        if cls:
            if cls in classes.values():
                return len(self.all(cls))
            else:
                return 0
        else:
            counts = {}
            for class_name, class_type in classes.items():
                counts[class_name] = len(self.all(class_type))
            return counts