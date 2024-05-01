#!/usr/bin/python3
""" create data for db"""

from models import storage
from models.place import Place
from models.user import User
from models.review import Review
from models.state import State
from models.city import City
from models.amenity import Amenity

state1 = State(name="Texas")
state1.save()

city1 = City(name="Houston", state_id=state1.id)
city1.save()

user1 = User(email="user@email.com", password="123")
user1.save()

place1 = Place(city_id=city1.id, user_id=user1.id, name="first place", number_rooms="2",
                number_bathrooms="1", max_guest="2", price_by_night="90")
place1.save()

amenity1 = Amenity(name="phone")
amenity1.save()

review1 = Review(place_id=place1.id, user_id=user1.id, text="good place")
review1.save()

storage.close()
