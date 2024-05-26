#!/usr/bin/python3
"""  """


import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from datetime import datetime

class TestGetCountMethods(unittest.TestCase):
    """
    Test case for get and count methods in storage classes.
    """

    def setUp(self):
        """
        Set up test cases.
        """
        self.file_storage = FileStorage()
        self.db_storage = DBStorage()
        self.obj1 = BaseModel(id='123', created_at=datetime.now(), updated_at=datetime.now())
        self.obj2 = BaseModel(id='456', created_at=datetime.now(), updated_at=datetime.now())
        self.file_storage.new(self.obj1)
        self.file_storage.new(self.obj2)
        self.db_storage.new(self.obj1)
        self.db_storage.new(self.obj2)

    def test_file_storage_get(self):
        """
        Test get method of FileStorage.
        """
        self.assertEqual(self.file_storage.get(BaseModel, '123'), self.obj1)
        self.assertIsNone(self.file_storage.get(BaseModel, '789'))

    def test_file_storage_count(self):
        """
        Test count method of FileStorage.
        """
        self.assertEqual(self.file_storage.count(), 2)
        self.assertEqual(self.file_storage.count(BaseModel), 2)

    def test_db_storage_get(self):
        """
        Test get method of DBStorage.
        """
        self.assertEqual(self.db_storage.get(BaseModel, '123'), self.obj1)
        self.assertIsNone(self.db_storage.get(BaseModel, '789'))

    def test_db_storage_count(self):
        """
        Test count method of DBStorage.
        """
        self.assertEqual(self.db_storage.count(), 2)
        self.assertEqual(self.db_storage.count(BaseModel), 2)


if __name__ == '__main__':
    unittest.main()