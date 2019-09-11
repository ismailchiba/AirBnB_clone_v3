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
from models import storage
import json
import os
import pep8
import unittest
import MySQLdb as SQLito
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

    def test_dbs_func_get(self):
        """Test for the presence of docstrings in DBStorage methods"""
        state = State(name="yesid")
        storage.new(state)
        storage.save()
        first_state_id = list(storage.all("State").values())[0].id
        id1 = first_state_id
        self.assertTrue(storage.get("State", first_state_id), id1)

    def test_dbs_func_count(self):
        """Test for the presence of docstrings in DBStorage methods"""
        num1 = storage.count("State")
        state = State(name="yesid")
        storage.new(state)
        storage.save()
        num2 = storage.count("State")
        first_state_id = list(storage.all("State").values())[0].id
        id1 = first_state_id
        self.assertTrue(storage.get("State", first_state_id), id1)
        self.assertTrue(num1 + 1, num2)

    def test_create_entry(self):
        """ Tests if a new element is added the db """
        os.system("cat setup_mysql_test.sql | mysql -hlocalhost -uroot -proot")
        connection = SQLito.connect(
            'localhost',
            'hbnb_test',
            'hbnb_test_pwd',
            'hbnb_test_db')
        cursor = connection.cursor()
        number1 = cursor.execute("SELECT * FROM states")
        cursor.execute(
            """INSERT INTO states(name, id, created_at, updated_at) VALUES\
                    ('California', '123456678', '2019-08-15T17:50:56.590977',\
                    '2019-08-15T17:50:56.590977')""")
        number2 = cursor.execute("SELECT * FROM states")
        self.assertEqual(number1 + 1, number2)


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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_fs_func_get(self):
        """Test for the presence of docstrings in DBStorage methods"""
        state = State(name="yesid")
        storage.new(state)
        storage.save()
        first_state_id = list(storage.all("State").values())[0].id
        id1 = first_state_id
        self.assertTrue(storage.get("State", first_state_id), id1)

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_fs_func_count(self):
        """Test for the presence of docstrings in DBStorage methods"""
        num1 = storage.count("State")
        state = State(name="yesid")
        storage.new(state)
        storage.save()
        num2 = storage.count("State")
        first_state_id = list(storage.all("State").values())[0].id
        id1 = first_state_id
        self.assertTrue(storage.get("State", first_state_id), id1)
        self.assertTrue(num1 + 1, num2)
