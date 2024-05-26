#!/usr/bin/python3
"""
Script that tests the functionality of the database storage.
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
    """
       This class tests the style and doc string of database
       storage class
    """
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
        result = pep8s.check_files(['tests/test_models/test_engine/test_db_storage.py'])
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
        """Test that all returns a dictionary"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        all_objs = models.storage.all()
        self.assertEqual(type(all_objs), dict)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_new(self):
        """Test that new adds an object to the database"""
        state = State(name="Texas")
        models.storage.new(state)
        self.assertIn(state, models.storage.all().values())

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        state = State(name="Washington")
        models.storage.new(state)
        models.storage.save()
        key = f"State.{state.id}"
        with open("file.json", "r") as f:
            json_data = json.load(f)
        self.assertIn(key, json_data)


@unittest.skipIf(models.storage_t != 'db', "not testing db storage")
class TestGetCountDB(unittest.TestCase):
    """testing get and count methods"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('...... Testing Get and Count ......')
        print('.......... DB Methods ..........')
        print('.................................\n\n')

    def setUp(self):
        """initializes new state and cities for testing"""
        self.state = State(name='California')
        self.state.save()
        self.city1 = City(name='Fremont', state_id=self.state.id)
        self.city1.save()
        self.city2 = City(name='San_Francisco', state_id=self.state.id)
        self.city2.save()

    def test_get(self):
        """Check if get method returns state"""
        real_state = models.storage.get("State", self.state.id)
        fake_state = models.storage.get("State", "12345")
        no_state = models.storage.get("", "")

        self.assertEqual(real_state, self.state)
        self.assertNotEqual(fake_state, self.state)
        self.assertIsNone(no_state)

    def test_count(self):
        """Check if count method returns correct numbers"""
        state_count = models.storage.count("State")
        city_count = models.storage.count("City")
        place_count = models.storage.count("Place")
        all_count = models.storage.count()

        self.assertEqual(state_count, 1)
        self.assertEqual(city_count, 2)
        self.assertEqual(place_count, 0)
        self.assertEqual(all_count, 3)


if __name__ == "__main__":
    unittest.main()
