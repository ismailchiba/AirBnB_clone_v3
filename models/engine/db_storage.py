#!/usr/bin/python3
"""
Contains the class DBStorage
"""

import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models import base_model, amenity, city, place, review, state, user


class DBStorage:
    """handles long term storage of all class instances"""
    classes = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        self.__engine = create_engine(
            'mysql+mysqldb://{}:{}@{}/{}'.format(
                os.environ.get('HBNB_MYSQL_USER'),
                os.environ.get('HBNB_MYSQL_PWD'),
                os.environ.get('HBNB_MYSQL_HOST'),
                os.environ.get('HBNB_MYSQL_DB')))
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """query on the current database session"""
        obj_dict = {}
        if cls:
            obj_class = self.__session.query(self.classes.get(cls)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
            return obj_dict
        for class_name in self.classes:
            if class_name == 'BaseModel':
                continue
            obj_class = self.__session.query(
                self.classes.get(class_name)).all()
            for item in obj_class:
                key = str(item.__class__.__name__) + "." + str(item.id)
                obj_dict[key] = item
        return obj_dict

    def get(self, cls, id):
        """
        fetches specific object
        :param cls: class of object as string
        :param id: id of object as string
        :return: found object or None
        """
        all_class = self.all(cls)

        for obj in all_class.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        count of how many instances of a class
        :param cls: class name
        :return: count of instances of a class
        """
        return len(self.all(cls))

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
