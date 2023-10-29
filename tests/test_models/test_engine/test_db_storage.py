#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from models.amenity import Amenity
from models.base_model import BaseModel
from models import storage
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from models.base_model import BaseModel
import json
import os
import pep8
import unittest
DBStorage = db_storage.DBStorage
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

    @unittest.skip('skip test for now')
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


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""
    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""


class TestDBStorageGet(unittest.TestCase):
    """  A test class for the 'get' method in DBStorage. """

    @unittest.skip('skip test for now')
    def setUpClass(cls):
        """
        Set up the test class for DBStorage.
        """
        # Initialize your DBStorage instance for testing
        cls.db_storage = DBStorage()
        cls.db_storage.reload()  # Load data for testing

    @classmethod
    def tearDownClass(cls):
        """
        Perform cleanup after all tests in the class have run.
        """
        # Perform any cleanup if needed
        pass

    def test_db_storage_get(self):
        """
        Test the get method in DBStorage.
        """
        # Test the get method in DBStorage
        # Replace 'YourModel' and 'your_id' with actual class and ID
        result = self.db_storage.get(YourModel, 'your_id')
        self.assertIsNotNone(result)
        # Add assertions to check if the object matches the expected object

class TestDBStorageCount(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """
        Set up the test class for DBStorage.
        """
        # Initialize your DBStorage instance for testing
        cls.db_storage = DBStorage()
        cls.db_storage.reload()  # Load data for testing

    @classmethod
    def tearDownClass(cls):
        """
        Perform cleanup after all tests in the class have run.
        """
        # Perform any cleanup if needed
        pass

    def test_db_storage_count(self):
        """
        Test the count method in DBStorage.
        """
        # Test the count method in DBStorage
        # Replace 'YourModel' with the actual class to count
        count = self.db_storage.count(YourModel)
        self.assertTrue(count >= 0)
