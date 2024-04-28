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
import pycodestyle
import unittest
from models import storage


FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pycodestyle_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_file_storage(self):
        """Test tests/test_models/
        test_file_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
        self.assertEqual(result.total_errors, 2,
                         "Found code style errors (and warnings).")

    def test_file_storage_module_docstring(self):
        """Test for the file_storage.py module docstring"""
        self.assertIsNot(file_storage.__doc__, None,
                         "file_storage.py needs a docstring")
        self.assertTrue(len(file_storage.__doc__) >= 1,
                        "file_storage.py needs a docstring")

    def test_file_storage_class_docstring(self):
        """Test for the FileStorage class docstring"""
        self.assertIsNot(FileStorage.__doc__, None,
                         "FileStorage class needs a docstring")
        self.assertTrue(len(FileStorage.__doc__) >= 1,
                        "FileStorage class needs a docstring")

    def test_fs_func_docstrings(self):
        """Test for the presence of docstrings in FileStorage methods"""
        for func in self.fs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        storage.reload()

    def tearDown(self):
        try:
            os.remove("file.json")
        except:
            pass

    def test_all(self):
        new_state = State(name="California")
        new_state.save()
        new_city = City(name="San Francisco", state_id=new_state.id)
        new_city.save()
        all_objs = storage.all()
        self.assertIn("State." + new_state.id, all_objs.keys())
        self.assertIn("City." + new_city.id, all_objs.keys())
        self.assertIn(new_state, all_objs.values())
        self.assertIn(new_city, all_objs.values())

    def test_all_with_cls(self):
        new_state = State(name="California")
        new_state.save()
        new_city = City(name="San Francisco", state_id=new_state.id)
        new_city.save()
        all_states = storage.all(State)
        self.assertIn("State." + new_state.id, all_states.keys())
        self.assertNotIn("City." + new_city.id, all_states.keys())
        self.assertIn(new_state, all_states.values())
        self.assertNotIn(new_city, all_states.values())

    def test_new(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        all_objs = storage.all(User)
        self.assertIn("User." + new_user.id, all_objs.keys())
        self.assertIn(new_user, all_objs.values())

    def test_save(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        all_objs = storage.all(User)
        self.assertIn("User." + new_user.id, all_objs.keys())

    def test_reload(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        storage.reload()
        all_objs = storage.all(User)
        self.assertIn("User." + new_user.id, all_objs.keys())

    def test_delete(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        storage.delete(new_user)
        all_objs = storage.all(User)
        self.assertNotIn("User." + new_user.id, all_objs.keys())

    def test_get(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        get_user = storage.get(User, new_user.id)
        self.assertEqual(get_user, new_user)

    def test_count(self):
        count_before = storage.count(User)
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        count_after = storage.count(User)
        self.assertEqual(count_after - count_before, 1)

if __name__ == "__main__":
    unittest.main()
