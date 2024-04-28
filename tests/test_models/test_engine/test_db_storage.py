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
import pycodestyle
import unittest
from models import storage


DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(DBStorage, inspect.isfunction)

    def test_pycodestyle_conformance_db_storage(self):
        """Test that models/engine/db_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['models/engine/db_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pycodestyle_conformance_test_db_storage(self):
        """Test tests/test_models/
        test_db_storage.py conforms to pycodestyle."""
        pycodestyles = pycodestyle.StyleGuide(quiet=True)
        result = pycodestyles.check_files(['tests/test_models/test_engine/\
test_db_storage.py'])
        self.assertEqual(result.total_errors, 2,
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


class TestDBStorage(unittest.TestCase):

    def setUp(self):
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'
        storage.reload()

    def tearDown(self):
        storage.close()
        os.environ['HBNB_ENV'] = 'test'
        os.environ['HBNB_MYSQL_USER'] = 'hbnb_test'
        os.environ['HBNB_MYSQL_PWD'] = 'hbnb_test_pwd'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'hbnb_test_db'

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

    def test_delete(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        storage.delete(new_user)
        all_objs = storage.all(User)
        self.assertNotIn("User." + new_user.id, all_objs.keys())

    def test_reload(self):
        new_user = User(email="test@example.com", password="test_pwd")
        storage.new(new_user)
        storage.save()
        storage.reload()
        all_objs = storage.all(User)
        self.assertIn("User." + new_user.id, all_objs.keys())

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

