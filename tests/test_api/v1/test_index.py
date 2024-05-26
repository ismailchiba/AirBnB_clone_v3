#!usr/bin/python3
""" Test index view """
import unittest
import os
import pep8
from models import storage
import api.v1.app


class TestIndex(unittest.TestCase):
    """ Test the index view """

    def setUp(self):
        api.v1.app.app.testing = True
        self.app = api.v1.app.app.test_client()

    def test_status(self):
        rv = self.app.get('api/v1/status')
        assert b'status' in rv.data
