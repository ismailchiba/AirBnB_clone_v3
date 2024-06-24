#!/usr/bin/python3
"""
Unit Test for Console Module
"""
import unittest
import console

HBNBCommand = console.HBNBCommand


class TestHBNBCommandDocs(unittest.TestCase):
    """Class for testing Console docs"""

    @classmethod
    def setUpClass(cls):
        print('\n\n.................................')
        print('..... Testing Documentation .....')
        print('.......  For the Console  .......')
        print('.................................\n\n')

    def test_doc_file(self):
        """Test for module documentation"""
        expected = 'This module contains the HBNBCommand class, the console of the HBNB project.'
        actual = console.__doc__
        self.assertEqual(expected, actual)

    def test_doc_class(self):
        """Test for class documentation"""
        expected = 'HBNBCommand class defines the console functionality.'
        actual = HBNBCommand.__doc__
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()
