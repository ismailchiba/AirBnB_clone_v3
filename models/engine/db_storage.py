#!/usr/bin/python3
"""
Contains the DBStorage class
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {
    "Amenity": Amenity, "BaseModel": Base, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class DBStorage:
    """
    Interacts with the MySQL database.

    Attributes:
        __engine (sqlalchemy.engine.Engine): The SQLAlchemy engine.
        __session (sqlalchemy.orm.scoped_session): The SQLAlchemy session.
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate a DBStorage object and create the engine.
        """
        self.__engine = create_engine(
            'mysql+mysqldb://<user>:<password>@<host>/<database>'
        )

    def all(self, cls=None):
        """
        Query on the current database session and return objects.

        Args:
            cls (type, optional): The class of the objects to lts to None.

        Returns:
            dict: A dictionary of queried obj the format <class name>.<id>.
        """
        if cls:
            objects = self.__session.query(cls).all()
        else:
            objects = []
            for class_name in classes.values():
                objects.extend(self.__session.query(class_name).all())
        return {f"{obj.__class__.__name__}.{obj.id}": obj for obj in objects}

    def new(self, obj):
        """
        Add the object to the current database session.

        Args:
            obj (BaseModel): The object to add.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session.

        Args:
            obj (BaseModel, optional): The object to delete. Defaults to None.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """
        Reload data from the database and create a new session.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                 bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def close(self):
        """
        Remove the current session.
        """
        self.__session.remove()

    def get(self, cls, id):
        """
        Retrieve one object based on class and its ID.

        Args:
            cls (type): The class of the object.
            id (str): The ID of the object.

        Returns:
            BaseModel: The object with the specified ID, or None if not found.
        """
        if cls and id:
            return self.__session.query(cls).filter_by(id=id).first()
        return None
