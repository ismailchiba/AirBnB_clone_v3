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
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Classes dictionary for object handling
classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User
}

class DBStorage:
    """Interacts with the MySQL database"""

    def __init__(self):
        """Initialize a DBStorage object"""
        self.__engine = None
        self.__session = None
        
        # Retrieve environment variables for DB connection
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        
        # Create the database engine
        self.__engine = create_engine(
            f"mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}"
        )

        # Drop tables if running in test environment
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reload data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(sess_factory)  # Correct indentation

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls == classes[clss] or cls == clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + "." + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete an object from the session if not None"""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """Close the session by calling remove() if session is initialized"""
        if self.__session:
            self.__session.remove()  # Indentation and syntax corrected
    
    def get(self, cls, obj_id):
        """Retrieve one object based on its class and ID."""
        if cls and obj_id:
            key = f"{cls.__name__}.{obj_id}"
            all_objects = self.all(cls)
            return all_objects.get(key, None)
        return None
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        '''get:
        retrieve an object from the file storage by class and id.
        '''
        if cls and id:
            if cls in classes.values() and isinstance(id, str):
                all_objects = self.all(cls)
                for key, value in all_objects.items():
                    if key.split('.')[1] == id:
                        return value
            else:
                return
        return

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls:
            if cls not in classes:  # Correct key reference
                return 0
            return len(self.all(cls))
        else:
            all_objects = self.all()
            return len(all_objects)

