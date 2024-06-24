#!/usr/bin/python3
"""
Unit Test for User Class
"""
import unittest
from datetime import datetime
import models
import json
import os

User = models.user.User
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class TestUserDocs(unittest.TestCase):
    """Class for testing User Class docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('........   User  Class   ........')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nUser Class from Models Module\n'
        actual = models.user.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'User class handles all application users'
        actual = User.__doc__
        self.assertEqual(expected, actual)


class TestUserInstances(unittest.TestCase):
    """Testing for User class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('.........  User  Class  .........')
        print('.................................\n\n')

    def setUp(self):
        """Initialize a new user for testing"""
        self.user = User()

    def test_instantiation(self):
        """Check if User is properly instantiated"""
        self.assertIsInstance(self.user, User)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """Check if User instantiation does not have updated attribute"""
        self.assertFalse(hasattr(self.user, 'updated_at'))

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """Check if save function adds updated_at attribute"""
        initial_time = self.user.updated_at
        self.user.save()
        updated_time = self.user.updated_at
        self.assertNotEqual(initial_time, updated_time)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """Check if to_json returns a serializable dict object"""
        self.user_json = self.user.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.user_json)
        except Exception:
            actual = 0
        self.assertEqual(1, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """Check if to_json includes class key with value User"""
        self.user_json = self.user.to_json()
        actual = None
        if self.user_json['__class__']:
            actual = self.user_json['__class__']
        expected = 'User'
        self.assertEqual(expected, actual)

    def test_email_attribute(self):
        """Add email attribute"""
        self.user.email = "bettyholbertn@gmail.com"
        if hasattr(self.user, 'email'):
            actual = self.user.email
        else:
            actual = ''
        expected = "bettyholbertn@gmail.com"
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
