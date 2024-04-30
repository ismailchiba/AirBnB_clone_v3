#!/usr/bin/python3
"""
Contains the FileStorage class
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def __init__(self):
        """Instantiate the class"""
        self.__models_available = {"User": User, "BaseModel": BaseModel,
                                   "Amenity": Amenity, "City": City,
                                   "Place": Place, "Review": Review,
                                   "State": State}
        self.reload()

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except Exception:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id_):
        """
        Retrieves one object
        @cls: Class name
        @id_: Object id.

        Returns: Object based on classs and it's id or None.
        """
        if not isinstance(cls, str):
            cls = cls.__name__
        if (cls not in classes.keys()) or (id_ is None):
            return None
        obj_count = self.all(cls)
        
        for obj_key, obj_value in obj_count.items():
            # Extract object ID from the key by splitting on '.'
            class_name, obj_id = obj_key.split('.')
            if obj_id.strip() == id_.strip():
                return obj_value
        return None

    def count(self, cls=None):
        """
        Number of objects in storage
        @cls: Class name(optional)

        Returns: Number of objects in storage or count of all
        storage objects if no class name parameter.
        """
        if cls is None:
            return len(self.__objects)
        
        if isinstance(cls, type):
            cls = cls.__name__

        if cls in classes:
            return len(self.all(cls))
        return -1
