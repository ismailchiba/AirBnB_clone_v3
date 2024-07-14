#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models import storage
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pycodestyle
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

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
        pep8s = pycodestyle.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_db_storage(self):
        """Test tests/test_models/test_db_storage.py conforms to PEP8."""
        pep8s = pycodestyle.StyleGuide(quiet=True)
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


# class TestDBStorageFunc(unittest.TestCase):
#     """Tests functionality of DBStorage"""

#     @classmethod
#     def setUpClass(cls):
#         """Set up for the entire test class"""
#         os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
#         os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
#         os.environ['HBNB_MYSQL_HOST'] = 'localhost'
#         os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
#         os.environ['HBNB_ENV'] = 'test'

#         cls.storage = DBStorage()
#         cls.storage.reload()

#         cls.state = State(name="TestState")
#         cls.user = User(email="test@example.com", password="password")

#         print(f"Creating State: {cls.state}")
#         print(f"Creating User: {cls.user}")

#         cls.storage.new(cls.state)
#         cls.storage.new(cls.user)
#         cls.storage.save()

#         print(f"State ID: {cls.state.id}")
#         print(f"User ID: {cls.user.id}")
#         print(f"{cls.storage.all()}")
#         print("State created:", cls.storage.get(State, cls.state.id))
#         print("User created:", cls.storage.get(User, cls.user.id))

#     @classmethod
#     def tearDownClass(cls):
#         """Tear down for the entire test class"""
#         cls.storage.delete(cls.state)
#         cls.storage.delete(cls.user)
#         cls.storage.save()
#         cls.storage._DBStorage__session.close()

#     def setUp(self):
#         """Set up for each individual test"""
#         self.session = self.storage._DBStorage__session

#     def tearDown(self):
#         """Clean up after each individual test"""
#         self.session.rollback()
#         for table in reversed(Base.metadata.sorted_tables):
#             self.session.execute(table.delete())
#         self.session.commit()

#     def test_get_existing_state(self):
#         """Test getting an existing State object"""
#         obj = self.storage.get('State', self.state.id)
#         self.assertIsNotNone(obj)
#         self.assertEqual(obj.id, self.state.id)
#         self.assertEqual(obj.name, "TestState")

#     def test_get_non_existing_state(self):
#         """Test getting a non-existing State object"""
#         obj = self.storage.get('State', 'non-existing-id')
#         self.assertIsNone(obj)

#     def test_get_existing_user(self):
#         """Test getting an existing User object"""
#         obj = self.storage.get('User', self.user.id)
#         self.assertIsNotNone(obj)
#         self.assertEqual(obj.id, self.user.id)
#         self.assertEqual(obj.email, "test@example.com")

#     def test_get_non_existing_user(self):
#         """Test getting a non-existing User object"""
#         obj = self.storage.get('User', 'non-existing-id')
#         self.assertIsNone(obj)


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
