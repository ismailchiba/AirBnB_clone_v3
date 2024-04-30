#!/usr/bin/python3

"""Contains the class DBStorage"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.state import State
from models.place import Place
from models.user import User
from models.city import City
from models.review import Review
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """A class that interacts with the MySQL database"""

    __engine = None
    __session = None

    def __init__(self):
        """A fn that Instantiate a DBStorage object"""

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
        """A query fn on the current database session"""

        n_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    n_dict[key] = obj
        return (n_dict)

    def new(self, obj):
        """A fn that add the object to the current DB session"""

        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current DB session"""

        self.__session.commit()

    def delete(self, obj=None):
        """A fn that delete from the current DB session obj if not None"""

        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """A fn that reloads data from the database"""

        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """Call remove() method on the private session attribute"""

        self.__session.remove()

    def get(self, cls=None, id=None):
        """A fn that returns obj based on class name and its ID"""

        if cls is not None and id is not None:
            try:
                return self.__session.query(classes[cls]).get(id)
            except Exception:
                return None

        return None

    def count(self, cls=None):
        """Returns the amount of objects"""

        if cls is not None:
            try:
                return len(self.all(classes[cls]))
            except Exception:
                return None
        else:
            return len(self.all())
