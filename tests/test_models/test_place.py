#!/usr/bin/python3
"""
Contains the TestPlaceDocs classes
"""

from datetime import datetime
import inspect
import models
from models import place
from models.base_model import BaseModel
import pep8
import unittest
from os import getenv

Place = place.Place


class TestPlaceDocs(unittest.TestCase):
    """Tests to check the documentation and style of Place class"""

    def __init__(self, *args, **kwargs):
        """
        Initialize a new Place instance with
        given arguments and keyword arguments.

        Attributes:
            name (str): The name of the model, set to 'Place'.
            value (class): The class reference for the model, set to Place.
        """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_city_id(self):
        """
        Test the type of 'city_id' attribute for a Place instance.

        Ensures that the 'city_id' attribute is a string.
        """
        new = self.value()
        new.city_id = "0001"
        self.assertEqual(type(new.city_id), str)

    def test_user_id(self):
        """
        Test the type of 'user_id' attribute for a Place instance.

        Ensures that the 'user_id' attribute is a string.
        """
        new = self.value()
        new.user_id = "0090"
        self.assertEqual(type(new.user_id), str)

    def test_name(self):
        """
        Test the type of 'name' attribute for a Place instance.

        Ensures that the 'name' attribute is a string.
        """
        new = self.value()
        new.name = "Name"
        self.assertEqual(type(new.name), str)

    def test_description(self):
        """
        Test the type of 'description' attribute for a Place instance.

        Ensures that the 'description' attribute is a string.
        """
        new = self.value()
        new.description = "description"
        self.assertEqual(type(new.description), str)

    def test_number_rooms(self):
        """
        Test the type of 'number_rooms' attribute for a Place instance.

        Ensures that the 'number_rooms' attribute is an integer.
        """
        new = self.value()
        new.number_rooms = 10
        self.assertEqual(type(new.number_rooms), int)

    def test_number_bathrooms(self):
        """
        Test the type of 'number_bathrooms' attribute for a Place instance.

        Ensures that the 'number_bathrooms' attribute is an integer.
        """
        new = self.value()
        new.number_bathrooms = 2
        self.assertEqual(type(new.number_bathrooms), int)

    def test_max_guest(self):
        """
        Test the type of 'max_guest' attribute for a Place instance.

        Ensures that the 'max_guest' attribute is an integer.
        """
        new = self.value()
        new.max_guest = 8
        self.assertEqual(type(new.max_guest), int)

    def test_price_by_night(self):
        """
        Test the type of 'price_by_night' attribute for a Place instance.

        Ensures that the 'price_by_night' attribute is an integer.
        """
        new = self.value()
        new.price_by_night = 90
        self.assertEqual(type(new.price_by_night), int)

    def test_latitude(self):
        """
        Test the type of 'latitude' attribute for a Place instance.

        Ensures that the 'latitude' attribute is a float.
        """
        new = self.value()
        new.latitude = -78.382324
        self.assertEqual(type(new.latitude), float)

    def test_longitude(self):
        """
        Test the type of 'longitude' attribute for a Place instance.

        Ensures that the 'longitude' attribute is a float.
        """
        new = self.value()
        new.longitude = 12.1923
        self.assertEqual(type(new.longitude), float)
    # def test_amenity_ids_files(self):
    #     """
    #     Test the 'amenities' attribute for a Place
    #     instance when using file storage.

    #     Ensures that the 'amenities' attribute is a
    #     list of strings representing amenity IDs.
    #     """
    #     new = self.value()
    #     new.amenities = ["wifi", "tv"]
    #     self.assertEqual(new.amenities[0], "wifi")

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Testeing to save")
    def test_amenity_ids(self):
        """Test that amenities can be added correctly."""
        from models.amenity import Amenity

        new = self.value()
        wifi = Amenity(name="wifi")
        tv = Amenity(name="tv")
        new.amenities.append(wifi)
        new.amenities.append(tv)
        self.assertTrue(isinstance(new.amenities, list))
        # Further checks can ensure that 'wifi' and 'tv'
        #  are indeed in amenities
        # self.assertIn(wifi, new.amenities)
        # self.assertIn(tv, new.amenities)

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.place_f = inspect.getmembers(Place, inspect.isfunction)

    def test_pep8_conformance_place(self):
        """Test that models/place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["models/place.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_place(self):
        """Test that tests/test_models/test_place.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["tests/test_models/test_place.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_place_module_docstring(self):
        """Test for the place.py module docstring"""
        self.assertIsNot(place.__doc__, None, "place.py needs a docstring")
        self.assertTrue(len(place.__doc__) >= 1, "place.py needs a docstring")

    def test_place_class_docstring(self):
        """Test for the Place class docstring"""
        self.assertIsNot(Place.__doc__, None, "Place class needs a docstring")
        self.assertTrue(
            len(Place.__doc__) >= 1, "Place class needs a docstring"
        )

    def test_place_func_docstrings(self):
        """Test for the presence of docstrings in Place methods"""
        for func in self.place_f:
            self.assertIsNot(
                func[1].__doc__,
                None,
                "{:s} method needs a docstring".format(func[0]),
            )
            self.assertTrue(
                len(func[1].__doc__) >= 1,
                "{:s} method needs a docstring".format(func[0]),
            )


class TestPlace(unittest.TestCase):
    """Test the Place class"""

    def test_is_subclass(self):
        """Test that Place is a subclass of BaseModel"""
        place = Place()
        self.assertIsInstance(place, BaseModel)
        self.assertTrue(hasattr(place, "id"))
        self.assertTrue(hasattr(place, "created_at"))
        self.assertTrue(hasattr(place, "updated_at"))

    def test_city_id_attr(self):
        """Test Place has attr city_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "city_id"))
        if models.storage_t == "db":
            self.assertEqual(place.city_id, None)
        else:
            self.assertEqual(place.city_id, "")

    def test_user_id_attr(self):
        """Test Place has attr user_id, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "user_id"))
        if models.storage_t == "db":
            self.assertEqual(place.user_id, None)
        else:
            self.assertEqual(place.user_id, "")

    def test_name_attr(self):
        """Test Place has attr name, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "name"))
        if models.storage_t == "db":
            self.assertEqual(place.name, None)
        else:
            self.assertEqual(place.name, "")

    def test_description_attr(self):
        """Test Place has attr description, and it's an empty string"""
        place = Place()
        self.assertTrue(hasattr(place, "description"))
        if models.storage_t == "db":
            self.assertEqual(place.description, None)
        else:
            self.assertEqual(place.description, "")

    def test_number_rooms_attr(self):
        """Test Place has attr number_rooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_rooms"))
        if models.storage_t == "db":
            self.assertEqual(place.number_rooms, None)
        else:
            self.assertEqual(type(place.number_rooms), int)
            self.assertEqual(place.number_rooms, 0)

    def test_number_bathrooms_attr(self):
        """Test Place has attr number_bathrooms, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "number_bathrooms"))
        if models.storage_t == "db":
            self.assertEqual(place.number_bathrooms, None)
        else:
            self.assertEqual(type(place.number_bathrooms), int)
            self.assertEqual(place.number_bathrooms, 0)

    def test_max_guest_attr(self):
        """Test Place has attr max_guest, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "max_guest"))
        if models.storage_t == "db":
            self.assertEqual(place.max_guest, None)
        else:
            self.assertEqual(type(place.max_guest), int)
            self.assertEqual(place.max_guest, 0)

    def test_price_by_night_attr(self):
        """Test Place has attr price_by_night, and it's an int == 0"""
        place = Place()
        self.assertTrue(hasattr(place, "price_by_night"))
        if models.storage_t == "db":
            self.assertEqual(place.price_by_night, None)
        else:
            self.assertEqual(type(place.price_by_night), int)
            self.assertEqual(place.price_by_night, 0)

    def test_latitude_attr(self):
        """Test Place has attr latitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "latitude"))
        if models.storage_t == "db":
            self.assertEqual(place.latitude, None)
        else:
            self.assertEqual(type(place.latitude), float)
            self.assertEqual(place.latitude, 0.0)

    def test_longitude_attr(self):
        """Test Place has attr longitude, and it's a float == 0.0"""
        place = Place()
        self.assertTrue(hasattr(place, "longitude"))
        if models.storage_t == "db":
            self.assertEqual(place.longitude, None)
        else:
            self.assertEqual(type(place.longitude), float)
            self.assertEqual(place.longitude, 0.0)

    @unittest.skipIf(models.storage_t == "db", "not testing File Storage")
    def test_amenity_ids_attr(self):
        """Test Place has attr amenity_ids, and it's an empty list"""
        place = Place()
        self.assertTrue(hasattr(place, "amenity_ids"))
        self.assertEqual(type(place.amenity_ids), list)
        self.assertEqual(len(place.amenity_ids), 0)

    def test_to_dict_creates_dict(self):
        """test to_dict method creates a dictionary with proper attrs"""
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(type(new_d), dict)
        self.assertFalse("_sa_instance_state" in new_d)
        for attr in p.__dict__:
            if attr is not "_sa_instance_state":
                self.assertTrue(attr in new_d)
        self.assertTrue("__class__" in new_d)

    def test_to_dict_values(self):
        """test that values in dict returned from to_dict are correct"""
        t_format = "%Y-%m-%dT%H:%M:%S.%f"
        p = Place()
        new_d = p.to_dict()
        self.assertEqual(new_d["__class__"], "Place")
        self.assertEqual(type(new_d["created_at"]), str)
        self.assertEqual(type(new_d["updated_at"]), str)
        self.assertEqual(new_d["created_at"], p.created_at.strftime(t_format))
        self.assertEqual(new_d["updated_at"], p.updated_at.strftime(t_format))

    def test_str(self):
        """test that the str method has the correct output"""
        place = Place()
        string = "[Place] ({}) {}".format(place.id, place.__dict__)
        self.assertEqual(string, str(place))
