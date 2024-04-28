#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
from distutils.dep_util import newer   # type: ignore
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
import sqlalchemy
import pep8  # type: ignore
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
        # Added April 2024
        new_obj = State('Idaho')
        self.assertEqual(new_obj.name, 'Idaho')

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    @unittest.skipIf(models.storage_t != 'db', 'not testing db storage')
    def test_check_storage(self):
        """Check if the storage is an instance of DbStorage. Added April 2024
        """
        self.assertTrue(isinstance(models.storage, DBStorage))

    @unittest.skipIf(models.storage_t != 'db')
    def test_check_dbstorage_attributes(self):
        """Check the storage attributes match for a new obj. Added April 2024
        """
        new_obj = User(email='okay@hello.com', password='HelloTheRe')
        self.assertTrue(new_obj.email, 'okay@hello.com')

    @unittest.skipIf(models.storage_t != 'db')
    def test_if_methods_exist(self):
        """Check if dbstorage has the following attributes. Added April 2024
        """
        self.assertTrue(hasattr(self.dbstorage, '__init__'))
        self.assertTrue(hasattr(self.dbstorage, 'all'))
        self.assertTrue(hasattr(self.dbstorage, 'new'))
        self.assertTrue(hasattr(self.dbstorage, 'save'))
        self.assertTrue(hasattr(self.dbstorage, 'delete'))

    @unittest.skipIf(models.storage_t != 'db')
    def test_check_delete(self):
        """Verify if delete works as expected. Added April 2024
        """
        new_obj = State('Delaware')
        models.storage.new(new_obj)
        save_id = new_obj.id
        key = 'User.{}'.format(save_id)
        self.assertIsInstance(new_obj, State)
        models.storage.save()
        old_result = models.storage.all("State")
        del_user_obj = old_result[key]
        models.storage.delete(del_user_obj)
        new_result = models.storage.all("State")
        self.assertNotEqual(len(old_result), len(new_result))
