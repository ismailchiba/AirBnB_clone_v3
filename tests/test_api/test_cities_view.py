#!/usr/bin/python3
""" Module containes tets for cities views/routes """

from api.v1.app import app
import unittest


class FlaskApiEndpointTests(unittest.TestCase):
    """ 
    class contains test for the flask app with api endpoints 
    """
    def setUp(self):
        """ sets up test_client """
        self.app = app.test_client()
    
    def test_index_view(self):
        """ """
        response = self.app.get('/api/v1/status')
        self.assertEqual(response.status_code, 200)
