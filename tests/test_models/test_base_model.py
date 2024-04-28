#!/usr/bin/python3
"""Test BaseModel for expected behavior and documentation"""
from datetime import datetime, timezone
import inspect
import models
import pep8
import time
import unittest
from unittest import mock
import json
import os
from os import getenv

BaseModel = models.base_model.BaseModel
module_doc = models.base_model.__doc__


class TestBaseModelDocs(unittest.TestCase):
    """Tests to check the documentation and style of BaseModel class"""

    def __init__(self, *args, **kwargs):
        """
        Initialize the TestBaseModelDocs instance.
        """
        super().__init__(*args, **kwargs)
        self.name = "BaseModel"
        self.value = BaseModel

    def setUp(self):
        """
        Set up method to configure the test environment before each test.
        """
        self.n = {"Name": "test"}

    def tearDown(self):
        """
        Tear down method to clean up after each test.
        """
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_default(self):
        """
        Test the default instantiation of a BaseModel.
        """
        i = self.value()
        self.assertEqual(type(i), self.value)

    def test_kwargs(self):
        """
        Test instantiation of a BaseModel with kwargs.
        """
        i = self.value()
        copy = i.to_dict()
        new = BaseModel(**copy)
        self.assertFalse(new is i)

    def test_kwargs_int(self):
        """
        Test instantiation of a BaseModel with
        kwargs containing non-string keys.
        """
        i = self.value()
        copy = i.to_dict()
        copy.update({1: 2})
        with self.assertRaises(TypeError):
            new = BaseModel(**copy)

    def test_save(self):
        """
        Test the save method of a BaseModel instance.
        """
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open("file.json", "r") as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_str(self):
        """
        Test the __str__ method of a BaseModel instance.
        """
        i = self.value()
        self.assertEqual(
            str(i), "[{}] ({}) {}".format(self.name, i.id, i.__dict__)
        )

    def test_todict(self):
        """
        Test the to_dict method of a BaseModel instance.
        """
        i = self.value()
        n = i.to_dict()
        self.assertEqual(i.to_dict(), n)

    def test_kwargs_types(self):
        """
        Test if attribute types remain the same when
        using kwargs to instantiate a BaseModel.
        """
        base_model = BaseModel()
        attribute_types_before = {
            key: type(getattr(base_model, key))
            for key in base_model.__dict__.keys()
        }
        base_model = BaseModel(
            id="test_id",
            __class__="BaseModel",
            created_at="2024-01-01T00:00:00.000000",
            updated_at="2024-01-01T00:00:00.000000",
        )
        attribute_types_after = {
            key: type(getattr(base_model, key))
            for key in base_model.__dict__.keys()
        }
        self.assertEqual(attribute_types_before, attribute_types_after)

    def test_empty_kwargs(self):
        """
        Test instantiation of a BaseModel with empty kwargs.
        """
        base_model = BaseModel()
        self.assertEqual(len(base_model.to_dict()), 4)

    def test_kwargs_none(self):
        """
        Test instantiation of a BaseModel with kwargs containing None.
        """
        n = {None: None}
        with self.assertRaises(TypeError):
            new = self.value(**n)

    def test_kwargs_one(self):
        """
        Test instantiation of a BaseModel with a single kwarg.
        """
        n = {"Name": "test"}
        with self.assertRaises(KeyError):
            new = self.value(**n)

    def test_id(self):
        """
        Test the id attribute of a BaseModel instance.
        """
        new = self.value()
        self.assertEqual(type(new.id), str)

    def test_created_at(self):
        """
        Test the created_at attribute of a BaseModel instance.
        """
        new = self.value()
        self.assertEqual(type(new.created_at), datetime)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Testeing to save")
    def test_save(self):
        """Testing save"""
        i = self.value()
        i.save()
        key = self.name + "." + i.id
        with open("file.json", "r") as f:
            j = json.load(f)
            self.assertEqual(j[key], i.to_dict())

    def test_kwargs_types(self):
        """Test if types remain the same as attribute
        types when using kwargs"""
        # Define a BaseModel instance with known attribute types
        base_model = BaseModel()
        attribute_types_before = {
            key: type(getattr(base_model, key))
            for key in base_model.__dict__.keys()
        }

        # Create a BaseModel instance with kwargs
        base_model = BaseModel(
            id="test_id",
            __class__="BaseModel",
            created_at="2024-01-01T00:00:00.000000",
            updated_at="2024-01-01T00:00:00.000000",
        )
        attribute_types_after = {
            key: type(getattr(base_model, key))
            for key in base_model.__dict__.keys()
        }

        # Compare attribute types before and after setting attributes
        self.assertEqual(attribute_types_before, attribute_types_after)

    def test_empty_kwargs(self):
        """Test if kwargs is empty"""
        base_model = BaseModel()
        self.assertEqual(len(base_model.to_dict()), 4)

    def test_updated_at(self):
        """
        Test that 'updated_at' is initialized correctly, and it remains
        unchanged upon creating a new instance from a
        dictionary representation.
        """
        # Create an instance of BaseModel
        instance = BaseModel()

        # Check if 'updated_at' is of type 'datetime'
        self.assertIsInstance(
            instance.updated_at,
            datetime,
            "updated_at should be a datetime object",
        )

        # Convert instance to a dictionary and create a new instance from it
        instance_dict = instance.to_dict()
        new_instance = BaseModel(**instance_dict)

        # Check if 'created_at' and 'updated_at' are equal for the new instance
        self.assertEqual(
            new_instance.created_at,
            new_instance.updated_at,
            "created_at and updated_at should be equal for a new\
                         instance created from a dictionary",
        )

    @classmethod
    def setUpClass(self):
        """Set up for docstring tests"""
        self.base_funcs = inspect.getmembers(BaseModel, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        for path in [
            "models/base_model.py",
            "tests/test_models/test_base_model.py",
        ]:
            with self.subTest(path=path):
                errors = pep8.Checker(path).check_all()
                self.assertEqual(errors, 0)

    def test_module_docstring(self):
        """Test for the existence of module docstring"""
        self.assertIsNot(module_doc, None, "base_model.py needs a docstring")
        self.assertTrue(len(module_doc) > 1, "base_model.py needs a docstring")

    def test_class_docstring(self):
        """Test for the BaseModel class docstring"""
        self.assertIsNot(
            BaseModel.__doc__, None, "BaseModel class needs a docstring"
        )
        self.assertTrue(
            len(BaseModel.__doc__) >= 1, "BaseModel class needs a docstring"
        )

    def test_func_docstrings(self):
        """Test for the presence of docstrings in BaseModel methods"""
        for func in self.base_funcs:
            with self.subTest(function=func):
                self.assertIsNot(
                    func[1].__doc__,
                    None,
                    "{:s} method needs a docstring".format(func[0]),
                )
                self.assertTrue(
                    len(func[1].__doc__) > 1,
                    "{:s} method needs a docstring".format(func[0]),
                )


class TestBaseModel(unittest.TestCase):
    """Test the BaseModel class"""

    def test_instantiation(self):
        """Test that object is correctly created"""
        inst = BaseModel()
        self.assertIs(type(inst), BaseModel)
        inst.name = "Holberton"
        inst.number = 89
        attrs_types = {
            "id": str,
            "created_at": datetime,
            "updated_at": datetime,
            "name": str,
            "number": int,
        }
        for attr, typ in attrs_types.items():
            with self.subTest(attr=attr, typ=typ):
                self.assertIn(attr, inst.__dict__)
                self.assertIs(type(inst.__dict__[attr]), typ)
        self.assertEqual(inst.name, "Holberton")
        self.assertEqual(inst.number, 89)

    def test_datetime_attributes(self):
        """Test that two BaseModel instances have different datetime objects
        and that upon creation have identical updated_at and created_at
        value."""
        tic = datetime.now(timezone.utc)
        inst1 = BaseModel()
        toc = datetime.now(timezone.utc)
        self.assertTrue(tic <= inst1.created_at <= toc)
        time.sleep(1e-4)
        tic = datetime.now(timezone.utc)
        inst2 = BaseModel()
        toc = datetime.now(timezone.utc)
        self.assertTrue(tic <= inst2.created_at <= toc)
        self.assertEqual(inst1.created_at, inst1.updated_at)
        self.assertEqual(inst2.created_at, inst2.updated_at)
        self.assertNotEqual(inst1.created_at, inst2.created_at)
        self.assertNotEqual(inst1.updated_at, inst2.updated_at)

    def test_uuid(self):
        """Test that id is a valid uuid"""
        inst1 = BaseModel()
        inst2 = BaseModel()
        for inst in [inst1, inst2]:
            uuid = inst.id
            with self.subTest(uuid=uuid):
                self.assertIs(type(uuid), str)
                self.assertRegex(
                    uuid,
                    "^[0-9a-f]{8}-[0-9a-f]{4}"
                    "-[0-9a-f]{4}-[0-9a-f]{4}"
                    "-[0-9a-f]{12}$",
                )
        self.assertNotEqual(inst1.id, inst2.id)

    def test_to_dict(self):
        """Test conversion of object attributes to dictionary for json"""
        my_model = BaseModel()
        my_model.name = "Holberton"
        my_model.my_number = 89
        d = my_model.to_dict()
        expected_attrs = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "my_number",
            "__class__",
        ]
        self.assertCountEqual(d.keys(), expected_attrs)
        self.assertEqual(d["__class__"], "BaseModel")
        self.assertEqual(d["name"], "Holberton")
        self.assertEqual(d["my_number"], 89)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        bm = BaseModel()
        new_d = bm.to_dict()
        self.assertEqual(new_d["__class__"], "BaseModel")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], bm.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], bm.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        inst = BaseModel()
        string = "[BaseModel] ({}) {}".format(inst.id, inst.__dict__)
        self.assertEqual(string, str(inst))

    @mock.patch("models.storage")
    def test_save(self, mock_storage):
        """Test that save method updates `updated_at` and calls
        `storage.save`"""
        inst = BaseModel()
        old_created_at = inst.created_at
        old_updated_at = inst.updated_at
        inst.save()
        new_created_at = inst.created_at
        new_updated_at = inst.updated_at
        self.assertNotEqual(old_updated_at, new_updated_at)
        self.assertEqual(old_created_at, new_created_at)
        self.assertTrue(mock_storage.new.called)
        self.assertTrue(mock_storage.save.called)
