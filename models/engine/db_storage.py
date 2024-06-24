#!/usr/bin/python3
"""
Contains the of class DBStorage
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

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class DBStorage:
    """interaacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv("HBNB_MYSQL_USER")
        HBNB_MYSQL_PWD = getenv("HBNB_MYSQL_PWD")
        HBNB_MYSQL_HOST = getenv("HBNB_MYSQL_HOST")
        HBNB_MYSQL_DB = getenv("HBNB_MYSQL_DB")
        HBNB_ENV = getenv("HBNB_ENV")
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}/{}".format(
                HBNB_MYSQL_USER, HBNB_MYSQL_PWD, HBNB_MYSQL_HOST, HBNB_MYSQL_DB
            )
        )
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def get(self, cls, id):
        """fetches specific object"""
        all_class = self.all(cls)

        for obj in all_class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """count of how many instances of a class"""
        return len(self.all(cls))

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        try:
            # Retrieve the state by ID
            if obj is not None:
                self.__session.delete(obj)
                self.__session.commit()
            else:
                pass
        except sqlalchemy.exc.InvalidRequestError as e:
            pass
        finally:
            self.__session.close()

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
        Query the database for the first instance
        of cls that has the given id.
        """
        # Use the class attribute to filter by id
        obj = self.__session.query(cls).filter(cls.id == id).first()
        return obj or None

    def count(self, cls=None):
        """
        A method to count the number of objects in storage.
        If cls is provided, count only objects of that class.
        """
        # Get all objects of  the cls if provided, otherwise all objects
        objects = self.all(cls) if cls else self.all()

        # Return the total count
        return len(objects)
