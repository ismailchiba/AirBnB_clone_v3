#!/usr/bin/python3
"""Defines the DBStorage engine."""

from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """Represents a database storage engine.

    Attributes:
        __engine (sqlalchemy.Engine): The SQLAlchemy engine.
        __session (sqlalchemy.Session): The SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """Initialize a new DBStorage instance."""
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(getenv("HBNB_MYSQL_USER"),
                                             getenv("HBNB_MYSQL_PWD"),
                                             getenv("HBNB_MYSQL_HOST"),
                                             getenv("HBNB_MYSQL_DB")),
                                      pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Query all objects in the current database session.

        Args:
            cls (class, optional): The class to query objects for.

        Returns:
            dict: A dictionary of queried objects.
        """
        classes = {"Amenity": Amenity, "City": City,
                   "Place": Place, "Review": Review,
                   "State": State, "User": User}
        if cls is None:
            objs = []
            for cls in classes:
                objs.extend(self.__session.query(classes[cls]).all())
        else:
            objs = self.__session.query(classes[cls]).all()
        return {"{}.{}".format(type(o).__name__, o.id): o for o in objs}

    def new(self, obj):
        """Add a new object to the current database session.

        Args:
            obj (BaseModel): The object to add.
        """
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the current database session.

        Args:
            obj (BaseModel, optional): The object to delete.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and initialize a new session."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """Close the current database session."""
        self.__session.close()
