#!/usr/bin/python3
"""
Unit tests for the Flask application
"""
import unittest
from api.v1.app import app
from flask import json

class TestApp(unittest.TestCase):
    """
    Test cases for the Flask application
    """
    def setUp(self):
        """
        Set up the test environment
        """
        self.app = app.test_client()

    def test_status_route(self):
        """
        Test the /status route
        """
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {"status": "OK"})

    def test_404_error(self):
        """
        Testing a non-existing route
        """
        response = self.app.get('/api/v1/non-existent')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json.loads(response.data), {"error": "Not found"})


if __name__ == '__main__':
    unittest.main()
