#!/usr/bin/python3
"""Defines the FileStorage class."""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class FileStorage:
    """Represents a file-based storage engine.

    Attributes:
        __file_path (str): The path to the JSON file storing objects.
        __objects (dict): A dictionary of objects keyed by class name and ID.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Retrieve all objects or objects of a specific class.

        Args:
            cls (class, optional): The class to filter objects.

        Returns:
            dict: A dictionary of objects.
        """
        if cls is not None:
            if isinstance(cls, str):
                cls = eval(cls)
            cls_dict = {}
            for key, obj in self.__objects.items():
                if isinstance(obj, cls):
                    cls_dict[key] = obj
            return cls_dict
        return self.__objects

    def new(self, obj):
        """Add a new object to the storage dictionary.

        Args:
            obj (BaseModel): The object to add.
        """
        self.__objects["{}.{}".format(type(obj).__name__, obj.id)] = obj

    def save(self):
        """Serialize the storage dictionary to a JSON file."""
        serialized_objs = {key: obj.to_dict()
                           for key, obj in self.__objects.items()}
        with open(self.__file_path, "w", encoding="utf-8") as file:
            json.dump(serialized_objs, file)

    def reload(self):
        """Deserialize the JSON file to populate the storage dictionary."""
        try:
            with open(self.__file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                for key, obj_data in data.items():
                    class_name, obj_id = key.split('.')
                    cls = eval(class_name)
                    self.__objects[key] = cls(**obj_data)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete an object from the storage dictionary.

        Args:
            obj (BaseModel, optional): The object to delete.
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(key, None)

    def close(self):
        """Reload data from file."""
        self.reload()
