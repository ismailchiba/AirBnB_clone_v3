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

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """interaacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
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
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def count(self, cls=None):
        """Count number of objects in based on class_name"""
        count = 0
        all_obj = []
        if cls is None:
            for cls in Base.__subclasses__():
                objs = self.__session.query(cls).all()
                for obj in objs:
                    all_obj.append(obj)
                    count += 1
            """print(len(all_obj))"""
            return count
        else:
            for clss in classes:
                if cls is classes[clss]:
                    objs = self.__session.query(classes[clss]).all()
                    for obj in objs:
                        if eval(obj.__class__.__name__) == cls:
                            all_obj.append(obj)
            return len(all_obj)

    def get(self, cls, id):
        """Return object based on class_name and Id"""
        for clss in classes:
            if cls is classes[clss]:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    if eval(obj.__class__.__name__) == cls and id == obj.id:
                        return (obj)
                    else:
                        return None

    def table_names(self):
        metadata = MetaData()
        metadata.reflect(bind=self.__engine)
        cls = []
        with self.__engine.connect() as connection:
            for table_name, table in metadata.tables.items():
                table_obj = Table(
                    table_name, metadata, autoload_with=self.__engine
                )
                """count = self.__engine.execute(table_obj.count()).scalar()"""
                if table_name == "place_amenity":
                    continue
                else:
                    cls.append(table_name)
            return cls

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
