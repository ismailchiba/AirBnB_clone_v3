#!/usr/bin/python3
"""
Unit Test for Review Class
"""
import unittest
from datetime import datetime
import models
import json
import os

Review = models.review.Review
BaseModel = models.base_model.BaseModel
storage_type = os.environ.get('HBNB_TYPE_STORAGE')


class TestReviewDocs(unittest.TestCase):
    """Class for testing Review docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......   Review  Class   .......')
        print('.................................\n\n')

    def test_doc_file(self):
        """... documentation for the file"""
        expected = '\nReview Class from Models Module\n'
        actual = models.review.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """... documentation for the class"""
        expected = 'Review class handles all application reviews'
        actual = Review.__doc__
        self.assertEqual(expected, actual)


class TestReviewInstances(unittest.TestCase):
    """Testing for Review class instances"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('....... Testing Functions .......')
        print('........  Review  Class  ........')
        print('.................................\n\n')

    def setUp(self):
        """Initialize a new review for testing"""
        self.review = Review()

    def test_instantiation(self):
        """Check if Review is properly instantiated"""
        self.assertIsInstance(self.review, Review)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_instantiation_no_updated(self):
        """Check if Review instantiation does not have updated attribute"""
        actual = self.review.updated_at
        self.assertIsNone(actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_updated_at(self):
        """Check if save function adds updated_at attribute"""
        initial_updated_at = self.review.updated_at
        self.review.save()
        updated_updated_at = self.review.updated_at
        self.assertNotEqual(initial_updated_at, updated_updated_at)
        self.assertIsInstance(updated_updated_at, datetime)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_to_json(self):
        """Check if to_json returns a serializable dict object"""
        self.review_json = self.review.to_json()
        actual = 1
        try:
            serialized = json.dumps(self.review_json)
        except Exception:
            actual = 0
        self.assertEqual(1, actual)

    @unittest.skipIf(storage_type == 'db', 'skip if environ is db')
    def test_json_class(self):
        """Check if to_json includes class key with value Review"""
        self.review_json = self.review.to_json()
        actual = None
        if self.review_json['__class__']:
            actual = self.review_json['__class__']
        expected = 'Review'
        self.assertEqual(expected, actual)

    def test_review_attribute(self):
        """Add review attribute"""
        self.review.text = "This place smells"
        if hasattr(self.review, 'text'):
            actual = self.review.text
        else:
            actual = ''
        expected = "This place smells"
        self.assertEqual(expected, actual)


if __name__ == '__main__':
    unittest.main()
