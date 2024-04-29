#!/usr/bin/python3
""" Database engine module """

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """Database storage engine"""

    # Dictionary to map class names to their corresponding classes
    CLASS_MAP = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    def __init__(self):
        """Initialize the database engine"""
        # Create the database engine
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        # If running in test mode, drop all tables
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieve all objects or objects of a specific class.

        Args:
            cls (str): The name of the class to retrieve objects for.

        Returns:
            dict: A dictionary containing all retrieved objects.
        """
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.CLASS_MAP.get(cls)).all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
            return obj_dict

        for class_name in self.CLASS_MAP:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(self.CLASS_MAP.get(class_name))
            .all()
            for item in obj_class:
                key = f"{item.__class__.__name__}.{item.id}"
                obj_dict[key] = item
        return obj_dict

    def new(self, obj):
        """
        Add a new object to the database session.

        Args:
            obj: The object to add to the session.
        """
        self.__session.add(obj)

    def get(self, cls, id):
        """
        Retrieve a specific object by class name and ID.

        Args:
            cls (str): The name of the class.
            id (str): The ID of the object.

        Returns:
            obj: The retrieved object, or None if not found.
        """
        all_class = self.all(cls)

        for obj in all_class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        Count the number of instances of a given class.

        Args:
            cls (str): The name of the class (optional).

        Returns:
            int: The number of instances of the class.
        """
        return len(self.all(cls))

    def save(self):
        """Commit all changes in the current database session."""
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete an object from the database session.

        Args:
            obj: The object to delete (optional).
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables in the database and reload session."""
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
            sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))

    def close(self):
        """Close the session."""
        self.__session.remove()
