#!/usr/bin/python3
"""
Testing Views for Index
Unittesting on index.py
"""


from api.v1.app import app
import unittest
import json
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.user import User
from models.state import State
from models.place import Place
from models import storage

class TestIndexView(unittest.TestCase):
    """
    The test cases for index.py
    """
    def setUp(self):
        """
        Setting up test environment
        """
        self.app = app.test_client()
        self.app.testing = True

    def test_stats(self):
        """
        Testing the route /stats
        """
        amenity = Amenity(name="Test Amenity")
        city = City(name="San Francisco", state_id=state.id)
        review = Review(place_id=place.id, user_id=user.id, text="Test Review")
        user = User(email="test@example.com", password="password")
        state = State(name="California")
        place = Place(city_id=city.id, user_id=user.id, name="Test Place")

        storage.new(amenity)
        storage.new(city)
        storage.new(review)
        storage.new(user)
        storage.new(state)
        storage.new(place)
        storage.save()

        response = self.app.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        stats = json.loads(response.data)

        self.assertEqual(stats["Amenity"], 1)
        self.assertEqual(stats["City"], 1)
        self.assertEqual(stats["Review"], 1)
        self.assertEqual(stats["User"], 1)
        self.assertEqual(stats["State"], 1)
        self.assertEqual(stats["Place"], 1)

    def tearDown(self):
        """
        Tearing down the environment testing
        """
        storage.reload()

if __name__ == '__main__':
    unittest.main()
