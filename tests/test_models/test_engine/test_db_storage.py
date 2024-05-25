#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
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


class TestDbStorage(unittest.TestCase):
    """Test the DB Storage class"""
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


class TestDBStorageGetMethod(unittest.TestCase):
    """ Test to test get method """
    def setUp(self):
        """ Set up test environment """
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """ Remove storage file at end of tests """
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_retrieve_existing_object(self):
        """ Retrieve an existing object by valid class and id """

        state = State(id="1234", name="California")
        self.storage.new(state)
        self.storage.save()

        result = self.storage.get(State, "1234")

        self.assertIsNotNone(result)
        self.assertEqual(result.id, "1234")
        self.assertEqual(result.name, "California")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_return_none_non_existent_id(self):
        """Return None when querying for a non-existent id with
            a valid class"""
        # Act
        result = self.storage.get(State, "9999")
        # Assert
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_invalid_class_type(self):
        """ Passing an invalid class type that does not exist in the database
            schema """

        class FakeClass:
            id = "78yr7yf"
        result = self.storage.get(FakeClass, "1234")
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_passing_none_as_class(self):
        """ Passing None as the class argument """

        result = self.storage.get(None, "1234")
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_correct_class_input(self):
        """ Correctly handle case where class is provided as a string name or
            class object"""

        state = State(id="1234", name="California")
        self.storage.new(state)
        self.storage.save()

        # Act
        result = self.storage.get("State", "1234")

        # Assert
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "1234")
        self.assertEqual(result.name, "California")

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_empty_or_invalid_id(self):
        """  Passing an empty string or invalid string as id """
        state = State(id="1234", name="California")
        self.storage.new(state)
        self.storage.save()

        result = self.storage.get(State, "")
        self.assertIsNone(result)


class TestDBStorageCountMethod(unittest.TestCase):
    """Tests for the count method of the DBStorage class."""
    def setUp(self):
        """ Set up test environment """
        self.storage = DBStorage()
        self.storage.reload()

    def tearDown(self):
        """ Remove storage file at end of tests """
        self.storage.close()

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_no_class(self):
        """
        Test that count method returns the total number of objects when
        cls is None.
        """
        expected_count = len(self.storage.all())
        actual_count = self.storage.count()
        self.assertEqual(actual_count, expected_count)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_empty_class(self):
        """
        Test that count method returns zero when the specified class has no
        instances in the database.
        """
        actual_count = self.storage.count(State)
        self.assertEqual(actual_count, 0)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_count_with_specified_class(self):
        """
        Test that count method returns the correct number of instances for
        a specified class.
        """
        # Create instances of a class
        self.storage.new(State(name="state1"))
        self.storage.new(State(name="state2"))
        self.storage.new(State(name="state3"))

        actual_count = self.storage.count(State)
        self.assertEqual(actual_count, 3)
