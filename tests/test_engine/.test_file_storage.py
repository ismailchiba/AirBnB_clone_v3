#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}

class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_get(self):
        """Test that the get method properly retrievs objects"""
        storage = FileStorage()
        self.assertIs(storage.get("User", "blah"), None)
        self.assertIs(storage.get("blah", "blah"), None)
        new_user = User()
        new_user.save()
        self.assertIs(storage.get("User", new_user.id), new_user)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "not testing file storage")
    def test_count(self):
        storage = FileStorage()
        initial_length = len(storage.all())
        self.assertEqual(storage.count(), initial_length)
        state_len = len(storage.all("State"))
        self.assertEqual(storage.count("State"), state_len)
        new_state = State()
        new_state.save()
        self.assertEqual(storage.count(), initial_length + 1)
        self.assertEqual(storage.count("State"), state_len + 1)
