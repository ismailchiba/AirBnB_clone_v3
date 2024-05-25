#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage, file_storage
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

DBStorage = db_storage.DBStorage
FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pep8_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        self.assertIsNot(db_storage.__doc__, None,
                         "db_storage.py needs a docstring")
        self.assertTrue(len(db_storage.__doc__) >= 1,
                        "db_storage.py needs a docstring")

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        self.assertIsNot(DBStorage.__doc__, None,
                         "DBStorage class needs a docstring")
        self.assertTrue(len(DBStorage.__doc__) >= 1,
                        "DBStorage class needs a docstring")

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in self.dbs_f:
            self.assertIsNot(func[1].__doc__, None,
                             "{:s} method needs a docstring".format(func[0]))
            self.assertTrue(len(func[1].__doc__) >= 1,
                            "{:s} method needs a docstring".format(func[0]))

    def test_get(self):
        """Test that get retrieves an object by class and id"""
        state = State(name="California")
        models.storage.new(state)
        models.storage.save()
        retrieved_state = models.storage.get("State", state.id)
        self.assertEqual(state, retrieved_state)

    def test_count(self):
        """Test that count returns the correct number of objects"""
        initial_count = models.storage.count("State")
        state = State(name="Nevada")
        models.storage.new(state)
        models.storage.save()
        new_count = models.storage.count("State")
        self.assertEqual(initial_count + 1, new_count)


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    def test_all_returns_dict(self):
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = models.storage.all()
        self.assertEqual(type(all_objs), dict)

    def test_new(self):
        """Test that new adds an object to the database"""
        state = State(name="Texas")
        models.storage.new(state)
        self.assertIn(state, models.storage.all().values())

    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = State(name="Washington")
        models.storage.new(state)
        models.storage.save()
        key = f"State.{state.id}"
        with open("file.json", "r") as f:
            json_data = json.load(f)
        self.assertIn(key, json_data)

    def test_get(self):
        """Test that get retrieves an object by class and id"""
        user = User(email="test@test.com", password="password")
        models.storage.new(user)
        models.storage.save()
        retrieved_user = models.storage.get("User", user.id)
        self.assertEqual(user, retrieved_user)

    def test_count(self):
        """Test that count returns the correct number of objects"""
        initial_count = models.storage.count("User")
        user = User(email="test2@test.com", password="password")
        models.storage.new(user)
        models.storage.save()
        new_count = models.storage.count("User")
        self.assertEqual(initial_count + 1, new_count)


if __name__ == "__main__":
    unittest.main()
