#!/usr/bin/python3
"""
Contains the TestFileStorageDocs classes
"""

from datetime import datetime
import inspect
import models
from models.engine import file_storage
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
        result = pep8s.check_files(['tests/test_models/test_engine/\
test_file_storage.py'])
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
    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_all_returns_dict(self):
        """Test that all returns the FileStorage.__objects attr"""
        storage = FileStorage()
        new_dict = storage.all()
        self.assertEqual(type(new_dict), dict)
        self.assertIs(new_dict, storage._FileStorage__objects)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_new(self):
        """test that new adds an object to the FileStorage.__objects attr"""
        storage = FileStorage()
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = {}
        test_dict = {}
        for key, value in classes.items():
            with self.subTest(key=key, value=value):
                instance = value()
                instance_key = instance.__class__.__name__ + "." + instance.id
                storage.new(instance)
                test_dict[instance_key] = instance
                self.assertEqual(test_dict, storage._FileStorage__objects)
        FileStorage._FileStorage__objects = save

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
        storage = FileStorage()
        new_dict = {}
        for key, value in classes.items():
            instance = value()
            instance_key = instance.__class__.__name__ + "." + instance.id
            new_dict[instance_key] = instance
        save = FileStorage._FileStorage__objects
        FileStorage._FileStorage__objects = new_dict
        storage.save()
        FileStorage._FileStorage__objects = save
        for key, value in new_dict.items():
            new_dict[key] = value.to_dict()
        string = json.dumps(new_dict)
        with open("file.json", "r") as f:
            js = f.read()
        self.assertEqual(json.loads(string), json.loads(js))


class TestFileGetMethod(unittest.TestCase):
    """ Test to test get method """
    def setUp(self):
        """ Set up test environment """
        self.storage = FileStorage()
        self.user = State(name="state1", id="123")
        self.storage.new(self.user)
        self.storage.save()

    def tearDown(self):
        """ Remove storage file at end of tests """
        self.storage.delete(self.user)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_retrieve_valid_object(self):
        """
        Test retrieving a valid object by class type and ID.
        """
        result = self.storage.get(State, "123")
        self.assertIsNotNone(result)
        self.assertEqual(result.id, "123")
        self.assertEqual(result.name, "state1")

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_return_none_no_match(self):
        """
        Test that None is returned when no object matches the specified
        class and ID.
        """
        result = self.storage.get(State, "999")
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_return_none_if_id_none(self):
        """
        Test that the get method returns None if the ID is None.

        This test ensures that when the ID is None, the get method returns
        None.
        """
        result = self.storage.get(State, None)
        self.assertIsNone(result)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_return_none_if_class_none(self):
        """
        Test that the get method returns None when the class type is None.
        """
        result = self.storage.get(None, "123")
        self.assertIsNone(result)


class TestFileCountMethod(unittest.TestCase):
    """Tests for the count method of the File Storage class."""

    def setUp(self):
        """ Set up test environment """
        self.storage = FileStorage()
        self.storage.reload()
        del_list = []
        for key in self.storage.all().keys():
            del_list.append(key)
        for key in del_list:
            self.storage.delete(self.storage.all()[key])

    def tearDown(self):
        """ Remove storage file at end of tests """
        self.storage.close
        if os.path.exists('file.json'):
            os.remove('file.json')

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_zero_when_no_objects(self):
        """
        Test that count method returns zero when no objects are stored.
        """
        self.assertEqual(self.storage.count(), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_all_objects_when_cls_is_none(self):
        """
        Test that count method returns the correct number of all objects when
        cls is None.
        """
        st1 = State(name="state1")
        self.storage.new(st1)
        pl1 = Place(firstname="Akin")
        self.storage.new(pl1)

        self.assertEqual(self.storage.count(), 2)
        self.assertEqual(self.storage.count(Place), 1)
        self.assertEqual(self.storage.count(State), 1)
        self
        self.storage.delete(st1)
        self.storage.delete(pl1)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_zero_for_no_instances_of_class(self):
        self.assertEqual(self.storage.count(User), 0)

    @unittest.skipIf(models.storage_t == 'db', "not testing file storage")
    def test_count_handles_nonexistent_classes(self):
        """
        Test if count method handles classes that do not exist.
        """
        class Origin:
            pass
        self.assertEqual(self.storage.count(Origin), 0)
