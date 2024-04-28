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
import MySQLdb
import json
import os
import pep8
import unittest
from models import storage
import os
DBStorage = db_storage.DBStorage
classes = {"Amenity": Amenity, "City": City, "Place": Place,
           "Review": Review, "State": State, "User": User}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    @classmethod
    def setUpClass(cls):
        """Set up the database once for all tests"""
        cls.db = MySQLdb.connect(user='hbnb_test',
                                 passwd='hbnb_test_pwd',
                                 db='hbnb_test_db',
                                 host="localhost",
                                 port=3306)
        cls.cursor = cls.db.cursor()

    def setUp(self):
        """ Create a static list of keys to iterate over"""
        all_objects = storage.all()
        keys_list = list(all_objects.keys())
        for obj_id in keys_list:
            storage.delete(all_objects[obj_id])
        storage.save()

    @classmethod
    def tearDownClass(cls):
        """Clean up the database after all tests"""
        if hasattr(cls, 'cursor') and cls.cursor:
            cls.cursor.execute("DROP DATABASE hbnb_test_db;")
            cls.db.commit()
            cls.cursor.close()
        if hasattr(cls, 'db') and cls.db:
            cls.db.close()

    def test_obj_list_empty(self):
        """ __objects is initially empty """
        self.assertEqual(len(storage.all()), 0)

    # def test_new(self):
    #     """ New object is correctly added to __objects """
    #     new = BaseModel()
    #     before_add = self.cursor.execute("""
    #         SELECT count(*) FROM baseModel
    #         GROUP BY (id)
    #     """)
    #     new.save()
    #     # Now checking if new object is in storage
    #     after_add = self.cursor.execute("""
    #         SELECT count(*) FROM baseModel
    #         GROUP BY (id)
    #     """)
    #     self.assertEqual(before_add + 1, after_add)
    # def test_all(self):
    #     """ __objects is properly returned """
    #     new = BaseModel()
    #     temp = storage.all()
    #     # Get the count of objects from the database
    #     self.cursor.execute("""
    #         SELECT count(*) FROM baseModel
    #         GROUP BY (id)
    #     """)
    #     db_all = len(self.cursor.fetchall())
    # Get the count of rows returned
    #     self.assertEqual(len(temp), db_all)

    # def test_base_model_instantiation(self):
    #     """ table is not created on BaseModel save """
    #     before_instance = self.cursor.execute(""""
    #                         SELECT count(*) From baseModel
    #                         GROUP BY (id)
    #                         """)
    #     new = BaseModel()
    #     after_instance = self.cursor.execute(""""
    #                         SELECT count(*) From baseModel
    #                         GROUP BY (id)
    #                         """)
    #     self.assertEqual(before_instance, after_instance)

    # def test_empty(self):
    #     """Data is not saved to database upon instance creation"""
    #     # Get the count of rows before creating a new object
    #     self.cursor.execute("SELECT COUNT(*) FROM baseModel;")
    #     before_create = self.cursor.fetchone()[0]
    #     # Create a new BaseModel instance without calling save
    #     new = BaseModel()
    #     # Count the number of rows after creating the new object
    #     self.cursor.execute("SELECT COUNT(*) FROM baseModel;")
    #     after_create = self.cursor.fetchone()[0]
    #     # Check that the number of rows remains the same,
    # indicating that the object was not saved to the database
    #     self.assertEqual(before_create, after_create)
    # def test_save(self):
    #     """DBStorage save method"""
    #     # Create a new BaseModel instance
    #     new = BaseModel()
    #     # Save the new instance using the storage
    #     storage.save(new)
    #     # Assuming you have a method to get the object
    # from storage, check if it exists
    #     retrieved_obj = storage.get(BaseModel, new.id)

    #     # Assert that the retrieved object is the same as the one we saved
    #     self.assertEqual(new, retrieved_obj)
    # def test_reload(self):
    #     """ Db is successfully loaded to __objects """
    #     new = BaseModel()
    #     new_id = new.id
    #     storage.save()
    #     storage.reload()
    #     _id = f'BaseModel.{new_id}'
    #     # Directly fetch the object by its unique ID after reloading
    #     reloaded_obj = storage.all()
    #     ob_id = f'{new.__class__.__name__}' + '.' + new.id
    #     # Ensure an object was returned after reload and it's the correct one
    #     self.assertIsNotNone(reloaded_obj,
    #                         "No object was loaded after reload.")
    # def test_reload_empty(self):
    #     """ Load from an empty db/table """
    #     with self.assertRaises(ValueError):
    #         storage.reload()

    # def test_reload_from_nonexistent(self):
    #     """ Nothing happens if db does not exist """
    #     self.assertEqual(storage.reload(), None)

    # def test_type_objects(self):
    #     """Confirm __objects is a dict"""
    #     self.assertIsInstance(storage.all(), dict,
    # "__objects is not a dictionary")
    # def test_key_format(self):
    #     """Key is properly formatted"""
    #     # Create a new BaseModel instance
    #     new = BaseModel()
    #     new.save()  # Save the object to ensure it's in storage
    #     _id = new.id
    #     expected_key = f'BaseModel.{_id}'
    #     # Check if the expected key is in the keys of storage
    #     self.assertIn(expected_key, storage.all().keys(),
    #                 f"Key {expected_key} not found in storage keys")

    # def test_storage_var_created(self):
    #     """Test if storage variable is an instance of DBStorage"""
    #     # Assuming storage is properly initialized before the test
    #     from models.engine.db_storage import DBStorage

    #     # Assert that storage is an instance of DBStorage
    #     self.assertIsInstance(storage, DBStorage,
    # "storage is not an instance of DBStorage")

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

    @unittest.skipIf(models.storage_t != 'db', "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""

    def test_get(self):
        """Test the get method."""
        user = User(email="test@example.com", password="test")
        self.storage.new(user)
        self.storage.save()
        self.assertEqual(self.storage.get(User, user.id), user)

    def test_count(self):
        """Test the count method."""
        initial_count = self.storage.count()
        self.storage.new(User(email="test@example.com", password="test"))
        self.storage.save()
        self.assertEqual(self.storage.count(), initial_count + 1)
        self.assertEqual(self.storage.count(User), 1)