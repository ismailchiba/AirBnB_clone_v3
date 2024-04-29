#!/usr/bin/python3
"""Unit tests for the state routes."""

import unittest
import json
from api.v1.app import app
from models.state import State
from models import storage


class TestStates(unittest.TestCase):
    """Test cases for state-related routes."""

    def setUp(self):
        """Set up test client and seed data."""
        self.client = app.test_client()
        self.test_state = State(name="Testland")
        storage.new(self.test_state)
        storage.save()

    def tearDown(self):
        """Clean up any mock data after tests."""
        storage.delete(self.test_state)
        storage.save()

    def test_lists_states(self):
        """Test retrieval of all states."""
        response = self.client.get("/api/v1/states")
        self.assertEqual(response.status_code, 200)

    def test_create_state(self):
        """Test creation of a new state."""
        response = self.client.post(
            "/api/v1/states",
            data=json.dumps({"name": "California"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        # Clean up created state
        created_state = json.loads(response.data.decode('utf-8'))
        storage.delete(State(**created_state))
        storage.save()

    def test_delete_state(self):
        """Test deletion of a state."""
        response = self.client.delete(f"/api/v1/states/{self.test_state.id}")
        self.assertEqual(response.status_code, 200)
        self.assertIsNone(storage.get(State, self.test_state.id))

    def test_get_state_by_id(self):
        """Test retrieval of a state by its ID."""
        response = self.client.get(f"/api/v1/states/{self.test_state.id}")
        self.assertEqual(response.status_code, 200)

    def test_update_state(self):
        """Test updating a state's name."""
        response = self.client.put(
            f"/api/v1/states/{self.test_state.id}",
            data=json.dumps({"name": "Newland"}),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        updated_state = storage.get(State, self.test_state.id)
        self.assertEqual(updated_state.name, "Newland")


if __name__ == "__main__":
    unittest.main()
