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

classes = {
    "Amenity": Amenity, "BaseModel": BaseModel, "City": City,
    "Place": Place, "Review": Review, "State": State, "User": User
}


class FileStorage:
    """
    Serializes instances to a JSON file & deserializes back to instances.

    Attributes:
        __file_path (str): Path to the JSON file.
        __objects (dict): Stores all objects by <class name>.id.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary __objects. , returns objects of that class.

        Args:
            cls (type, optional): The class of the objects to return. Defaults.

        Returns:
            dict: A dictionary of all objects, or objects of a speif cls
        """
        if cls is not None:
            new_dict = {
                key: value for key, value in self.__objects.items()
                if isinstance(value, cls) or value.__class__.__name__ == cls
            }
            return new_dict
        return self.__objects

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id.

        Args:
            obj (BaseModel): The object to add to __objects.
        """
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path).
        """
        json_objects = {
            key: obj.to_dict() for key, obj in self.__objects.items()
        }
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key, value in jo.items():
                self.__objects[key] = classes[value["__class__"]](**value)
        except Exception:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside.

        Args:
            obj (BaseModel, optional): The object to delete. Defaults to None.
        """
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """
        Call reload() method for deserializing the JSON file to objects.
        """
        self.reload()

    def get(self, cls, id):
        """
        Retrieve one object based on class and its ID.

        Args:
            cls (type): The class of the object.
            id (str): The ID of the object.

        Returns:
            BaseModel: The object with the specified class and ID, or None
        """
        if cls and id:
            key = "{}.{}".format(cls.__name__, id)
            return self.__objects.get(key)
        return None

    def count(self, cls=None):
        """
        Count the number of objects in storage. Iunts objects of that class.

        Args:
            cls (type, optional): The class of the objects to countto None.

        Returns:
            int: The number of objects of a specific class if cls is provided.
        """
        if cls:
            return len([obj for obj in self.__objects.values()
                       if isinstance(obj, cls)])
        return len(self.__objects)
