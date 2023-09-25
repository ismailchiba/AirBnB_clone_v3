#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

import inspect
import models
from models.engine import file_storage
from models.engine.file_storage import FileStorage
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

FileStorage = file_storage.FileStorage
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class TestFileStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of FileStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.fs_f = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_pep8_conformance_file_storage(self):
        """Test that models/engine/file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['models/engine/file_storage.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_file_storage(self):
        """Test tests/test_models/test_file_storage.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_models/test_engine/'
                                   'test_file_storage.py'])
        self.assertEqual(result.total_errors, 0,
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
    """Test the FileStorage class"""

    def setUp(self):
        """Set up before each test."""
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        new_dict = self.storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, self.storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        save = self.storage._FileStorage__objects
        self.storage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                self.storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, self.storage._FileStorage__objects)
        self.storage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = self.storage._FileStorage__objects
        self.storage._FileStorage__objects = new_dict
        self.storage.save()
        self.storage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


class TestFileStorageGet(unittest.TestCase):
    """Test the get method in FileStorage"""

    def test_get(self):
        """Test the get method"""
        # Create an instance of FileStorage
        storage = FileStorage()

        # Create a test object (e.g., an Amenity instance)
        test_obj = Amenity(name="Test Amenity")
        test_obj.save()

        # Use the get method to retrieve the test object
        retrieved_obj = storage.get(Amenity, test_obj.id)

        # Assert that the retrieved object is not None
        self.assertIsNotNone(retrieved_obj)

        # Assert that the retrieved object has the correct class and ID
        self.assertIsInstance(retrieved_obj, Amenity)
        self.assertEqual(retrieved_obj.id, test_obj.id)


class TestFileStorageCount(unittest.TestCase):
    """Test the count method in FileStorage"""

    def test_count(self):
        """Test the count method"""
        # Create an instance of FileStorage
        storage = FileStorage()

        # Create some test objects (e.g., Amenity instances)
        amenity1 = Amenity(name="Amenity 1")
        amenity2 = Amenity(name="Amenity 2")
        amenity3 = Amenity(name="Amenity 3")

        # Save the test objects
        amenity1.save()
        amenity2.save()
        amenity3.save()

        # Use the count method to count all Amenity objects
        count_all = storage.count(Amenity)

        # Assert that the count is correct
        self.assertEqual(count_all, 3)

        # Use the count method to count all objects (no class specified)
        count_all_objects = storage.count()

        # Assert that the count of all objects is correct
        self.assertEqual(count_all_objects, 3)


if __name__ == '__main__':
    unittest.main()
