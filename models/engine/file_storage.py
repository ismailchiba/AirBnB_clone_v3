#!/usr/bin/python3
"""Contains the FileStorage class"""

import json
from models import base_model, amenity, city, place, review, state, user
from datetime import datetime

strptime = datetime.strptime
to_json = base_model.BaseModel.to_json


class FileStorage:
    """handles long term storage of all class instances"""
    Classmap = {
        'BaseModel': base_model.BaseModel,
        'Amenity': amenity.Amenity,
        'City': city.City,
        'Place': place.Place,
        'Review': review.Review,
        'State': state.State,
        'User': user.User
    }
    
    """serializes instances to a JSON file & deserializes back to instances"""
    __file_path = "./dev/file.json"
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            obj_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    obj_dict[key] = value
            return obj_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        key = "{}.{}".format(type(obj).__name__, obj.id)
        self.__objects[key] = obj

    def get(self, cls, id):
        """method to retrieve one object"""
        all_class = self.all(cls)
        """ilterate over each object"""
        for obj in all_class.values():
            if id == str(obj.id):
                return (obj)
        """if no matching object is found return none"""
        return (None)    

    def count(self, cls=None):
        """count number of object in storage"""
        return len(self.all(cls))

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, mode='w+', encoding='utf-8') as f:
            json.dump(json_objects, f)

    def reload(self):
        """deserializes the JSON file to __objects"""
        fname = self.__file_path
        self.__objects = {}
        try:
            with open(fname, mode='r', encoding='utf-8') as f:
                new_obj = json.load(f)
        except:
            return
        for obj_id, date in new_obj.items():
            k_cls = date['__class__']
            date.pop("__class__", None)
            date["created_at"] = datetime.strptime(date["created_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            date["updated_at"] = datetime.strptime(date["updated_at"],
                                                "%Y-%m-%d %H:%M:%S.%f")
            self.__objects[obj_id] = self.Classmap[k_cls](**date)

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
