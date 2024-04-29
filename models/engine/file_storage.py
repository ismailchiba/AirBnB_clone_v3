#!/usr/bin/python3

"""
Contains the FileStorage class
"""

import json

from models import base_model
from models import amenity
from models import city
from models import place
from models import review
from models import state
from models import user

from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """
    Handling long term storage of all class instances
    """

    CNC = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }

    """
    CNC => A dictionary with:
        keys: Class Names
        values: Class type (used for instantiation)
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Retrieves all objects from the database
        """

        if cls:
            objects_dict = {}
            for class_id, obj in FileStorage.__objects.items():
                if type(obj).__name__ == cls:
                    objects_dict[class_id] = obj
            return objects_dict
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the current session
        """

        basemodel_id = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[basemodel_id] = obj

    def get(self, cls, id):
        """
        Retrieves a specific object
        """

        all_classes = self.all(cls)

        for obj in all_classes.values():
            if id == str(obj.id):
                return obj

        return None

    def count(self, cls=None):
        """
        Counts the number of instances of a class
        """

        return len(self.all(cls))

    def save(self):
        """
        Commits all changes in the current database session
        """

        file_name = FileStorage.__file_path
        dictionary = {}

        for basemodel_id, basemodel_obj in FileStorage.__objects.items():
            dictionary[basemodel_id] = basemodel_obj.to_json()
        with open(file_name, mode='w+', encoding='utf-8') as f_io:
            json.dump(dictionary, f_io)

    def reload(self):
        """
        Creates all database tables & initializes new database session
        """

        file_name = FileStorage.__file_path
        FileStorage.__objects = {}

        try:
            with open(file_name, mode='r', encoding='utf-8') as f_io:
                new_objs = json.load(f_io)
        except Exception:
            return
        for object_id, dictionary in new_objs.items():
            k_cls = dictionary['__class__']
            dictionary.pop("__class__", None)
            dictionary["created_at"] = datetime.strptime(
                dictionary["created_at"], "%Y-%m-%d %H:%M:%S.%f")

            dictionary["updated_at"] = datetime.strptime(
                dictionary["updated_at"], "%Y-%m-%d %H:%M:%S.%f")

            FileStorage.__objects[object_id] = FileStorage.CNC[k_cls](
                **dictionary)

    def delete(self, obj=None):
        """
        Deletes an object from the current session
        """
        if obj is None:
            return
        for key in list(FileStorage.__objects.keys()):
            if obj.id == key.split(".")[1] and key.split(".")[0] in str(obj):
                FileStorage.__objects.pop(key, None)
                self.save()

    def close(self):
        """
        Closes the current session
        """
        self.reload()
