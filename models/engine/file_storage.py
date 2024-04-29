#!/usr/bin/python3
"""
Handles I/O, writing and reading, of JSON for storage of all class instances
"""
import json
from datetime import datetime
from models import base_model, amenity, city, place, review, state, user


class FileStorage:
    """
    Handles long-term storage of all class instances
    """

    # Class-Name-to-Class mapping dictionary
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
        """Initialize FileStorage"""
        self.__file_path = './dev/file.json'
        self.__objects = {}

    def all(self, cls=None):
        """
        Retrieve all objects or objects of a specific class.

        Args:
            cls (str): The name of the class to retrieve objects for.

        Returns:
            dict: A dictionary containing all retrieved objects.
        """
        if cls:
            objects_dict = {}
            for class_id, obj in self.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return self.__objects

    def new(self, obj):
        """
        Add a new object to the storage.

        Args:
            obj: The object to add to storage.
        """
        obj_key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[obj_key] = obj

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
        """Serialize objects to the JSON file"""
        data = {}
        for obj_key, obj in self.__objects.items():
            data[obj_key] = obj.to_json()

        with open(self.__file_path, 'w') as file:
            json.dump(data, file)

    def reload(self):
        """Deserialize JSON file to objects"""
        try:
            with open(self.__file_path, 'r') as file:
                data = json.load(file)
        except FileNotFoundError:
            return

        self.__objects = {}
        for obj_key, obj_data in data.items():
            class_name = obj_data['__class__']
            obj_data.pop("__class__", None)
            obj_data['created_at'] = datetime.strptime(obj_data['created_at'],
                                                       '%Y-%m-%d %H:%M:%S.%f')
            obj_data['updated_at'] = datetime.strptime(obj_data['updated_at'],
                                                       '%Y-%m-%d %H:%M:%S.%f')

            obj = FileStorage.CLASS_MAP[class_name](**obj_data)
            self.__objects[obj_key] = obj

    def delete(self, obj=None):
        """Delete object from storage"""
        if obj:
            obj_key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects.pop(obj_key, None)
            self.save()

    def close(self):
        """Reload data from JSON file"""
        self.reload()
