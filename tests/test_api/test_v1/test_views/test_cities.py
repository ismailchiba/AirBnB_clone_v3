#!/usr/bin/python3
"""
Unit tests for the City view
"""
from api.v1.app import app
import json
import unittest
from models.city import City
from models.state import State
from models import storage


class TestCityView(unittest.TestCase):
    """Testing City view cases"""

    def setUp(self):
        """Setting up the environment for testing"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_cities(self):
        """Test up GET /api/v1/states/<state_id>/cities route"""
        state = State(name="California")
        state.save()
        city = City(name="San Francisco", state_id=state.id)
        city.save()
        response = self.app.get(f'/api/v1/states/{state.id}/cities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(json.loads(response.data)), list)
        self.assertEqual(len(json.loads(response.data)), 1)

    def test_get_cities_state_not_found(self):
        """Testing GET /api/v1/states/<state_id>/cities route invalid state_id"""
        response = self.app.get('/api/v1/states/invalid_id/cities')
        self.assertEqual(response.status_code, 404)

    def test_get_city(self):
        """Test up GET /api/v1/cities/<city_id> route"""
        state = State(name="California")
        state.save()
        city = City(name="San Francisco", state_id=state.id)
        city.save()
        response = self.app.get(f'/api/v1/cities/{city.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], "San Francisco")

    def test_get_city_not_found(self):
        """Testing GET /api/v1/cities/<city_id> route invalid ID"""
        response = self.app.get('/api/v1/cities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_city(self):
        """Test the DELETE /api/v1/cities/<city_id> route"""
        state = State(name="California")
        state.save()
