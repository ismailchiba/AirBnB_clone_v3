#!/usr/bin/python3
"""
Unittesting for this State object
"""
from api.v1.app import app
import json
import unittest
from models.state import State
from models import storage


class TestStateView(unittest.TestCase):
    """Testing the cases for the State"""

    def setUp(self):
        """Setting up the test environment"""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_states(self):
        """Testing the GET route /api/v1/states"""
        response = self.app.get('/api/v1/states')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(json.loads(response.data)), list)

    def test_get_state(self):
        """Testing the GET route /api/v1/states/<state_id>"""
        state = State(name="California")
        state.save()
        response = self.app.get(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], "California")

    def test_get_state_not_found(self):
        """Testing the GET route /api/v1/states/<state_id> with an invalid ID"""
        response = self.app.get('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_delete_state(self):
        """Testing the DELETE route /api/v1/states/<state_id>"""
        state = State(name="California")
        state.save()
        response = self.app.delete(f'/api/v1/states/{state.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data), {})
        self.assertIsNone(storage.get(State, state.id))

    def test_delete_state_not_found(self):
        """Testing the DELETE route with an invalid ID /api/v1/states/<state_id>"""
        response = self.app.delete('/api/v1/states/invalid_id')
        self.assertEqual(response.status_code, 404)

    def test_create_state(self):
        """Testing the POST /api/v1/states route"""
        data = {"name": "New York"}
        response = self.app.post('/api/v1/states', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', json.loads(response.data))
        self.assertEqual(json.loads(response.data)['name'], "New York")

    def test_create_state_missing_name(self):
        """Testing the POST /api/v1/states route with missing name"""
        data = {}
        response = self.app.post('/api/v1/states', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Missing name"})

    def test_create_state_invalid_json(self):
        """Testing the POST /api/v1/states route with invalid JSON data"""
        data = "invalid_data"
        response = self.app.post('/api/v1/states', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Not a JSON"})

    def test_update_state(self):
        """Testing the PUT /api/v1/states/<state_id> route"""
        state = State(name="California")
        state.save()
        data = {"name": "New California"}
        response = self.app.put(f'/api/v1/states/{state.id}', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data)['name'], "New California")

    def test_update_state_not_found(self):
        """Testing the PUT /api/v1/states/<state_id> route with an invalid ID"""
        data = {"name": "New California"}
        response = self.app.put('/api/v1/states/invalid_id', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 404)

    def test_update_state_invalid_json(self):
        """Testing the PUT /api/v1/states/<state_id> route with invalid JSON data"""
        state = State(name="California")
        state.save()
        data = "invalid_data"
        response = self.app.put(f'/api/v1/states/{state.id}', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.data), {"error": "Not a JSON"})

    def tearDown(self):
        """Tear down the test environment"""
        storage.reload()

if __name__ == '__main__':
    unittest.main()
