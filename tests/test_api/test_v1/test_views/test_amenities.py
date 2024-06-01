#!/usr/bin/python3
"""
Unit tests for the Amenity view
"""
from api.v1.app import app
import json
import unittest
from models.amenity import Amenity
from models import storage


class TestAmenityView(unittest.TestCase):
    """Testing Amenity view cases"""

    def setUp(self):
        """Setting up the environment"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_amenities(self):
        """Test the GET /api/v1/amenities route"""
        response = self.app.get('/api/v1/amenities')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(json.loads(response.data)), list)

    def test_get_amenity(self):
        """Test the GET /api/v1/amenities/<amenity_id> route"""
        amenity = Amenity(name="Wifi")
        amenity.save()
        response = self.app.get(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], "Wifi")

    def test_get_amenity_not_found(self):
        """Test the GET /api/v1/amenities/<amenity_id> route with an invalid ID"""
        response = self.app.get('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_amenity(self):
        """Test the DELETE /api/v1/amenities/<amenity_id> route"""
        amenity = Amenity(name="Wifi")
        amenity.save()
        response = self.app.delete(f'/api/v1/amenities/{amenity.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {})
        self.assertIsNone(storage.get(Amenity, amenity.id))

    def test_delete_amenity_not_found(self):
        """Test the DELETE /api/v1/amenities/<amenity_id> route with an invalid ID"""
        response = self.app.delete('/api/v1/amenities/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_amenity(self):
        """Test the POST /api/v1/amenities route"""
        data = {"name": "Wifi"}
        response = self.app.post('/api/v1/amenities', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))
        self.assertEqual(json.loads(response.data)['name'], "Wifi")

    def test_create_amenity_missing_name(self):
        """Test the POST /api/v1/amenities route with missing name"""
        data = {}
        response = self.app.post('/api/v1/amenities', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Missing name"})

    def test_create_amenity_invalid_json(self):
        """Test the POST /api/v1/amenities route with invalid JSON data"""
        data = "invalid_data"
        response = self.app.post('/api/v1/amenities', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Not a JSON"})

    def test_update_amenity(self):
        """Test the PUT /api/v1/amenities/<amenity_id> route"""
        amenity = Amenity(name="Wifi")
        amenity.save()
        data = {"name": "High-Speed Wifi"}
        response = self.app.put(f'/api/v1/amenities/{amenity.id}', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], "High-Speed Wifi")

    def test_update_amenity_not_found(self):
        """Test the PUT /api/v1/amenities/<amenity_id> route with an invalid ID"""
        data = {"name": "High-Speed Wifi"}
        response = self.app.put('/api/v1/amenities/invalid_id', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity_invalid_json(self):
        """Test the PUT /api/v1/amenities/<amenity_id> route with invalid JSON data"""
        amenity = Amenity(name="Wifi")
        amenity.save()
        data = "invalid_data"
        response = self.app.put(f'/api/v1/amenities/{amenity.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Not a JSON"})

    def tearDown(self):
        """Tear down the test environment"""
        storage.reload()

if __name__ == '__main__':
    unittest.main()
