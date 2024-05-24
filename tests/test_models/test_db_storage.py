import unittest
import os
from unittest.mock import patch
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        if os.getenv('HBNB_ENV') == 'test':
            DBStorage().reload()

    def setUp(self):
        self.storage = DBStorage()
        self.obj = BaseModel()

    def tearDown(self):
        self.storage.close()

    def test_init(self):
        self.assertIsInstance(self.storage.__engine, create_engine)
        if os.getenv('HBNB_ENV') == 'test':
            self.assertEqual(self.storage.__session.query(BaseModel).count(), 0)
            self.storage.new(self.obj)
            self.assertEqual(self.storage.__session.query(BaseModel).count(), 1)

    def test_all(self):
        self.assertEqual(self.storage.all().__len__(), 0)
        self.storage.new(self.obj)
        self.assertEqual(self.storage.all().__len__(), 1)
        self.assertEqual(self.storage.all(BaseModel).__len__(), 1)
        with self.assertRaises(AttributeError):
            self.storage.all('User')

    def test_new(self):
        self.storage.new(self.obj)
        self.assertEqual(self.storage.__session.query(BaseModel).count(), 1)

    def test_save(self):
        self.storage.new(self.obj)
        self.storage.save()
        self.storage.new(self.obj)
        self.storage.save()
        self.assertEqual(self.storage.__session.query(BaseModel).count(), 2)

    def test_delete(self):
        self.storage.new(self.obj)
        self.storage.save()
        self.storage.delete(self.obj)
        self.storage.save()
        self.assertEqual(self.storage.__session.query(BaseModel).count(), 0)

    def test_reload(self):
        self.storage.reload()
        self.assertIsInstance(self.storage.__session, scoped_session)
        self.assertEqual(self.storage.__session.query(BaseModel).count(), 0)
        self.storage.new(self.obj)
        self.storage.save()
        self.storage.reload()
        self.assertEqual(self.storage.__session.query(BaseModel).count(), 1)

    def test_get(self):
        self.storage.new(self.obj)
        self.storage.save()
        obj = self.storage.get(BaseModel, self.obj.id)
        self.assertEqual(obj.id, self.obj.id)

    def test_count(self):
        self.assertEqual(self.storage.count(), 0)
        self.storage.new(self.obj)
        self.assertEqual(self.storage.count(), 1)
        self.assertEqual(self.storage.count(BaseModel), 1)
        with self.assertRaises(AttributeError):
            self.storage.count('User')


