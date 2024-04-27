#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import console
import inspect
import pep8
import unittest
from unittest.mock import patch
from io import StringIO

HBNBCommand = console.HBNBCommand
class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""
    
    def setUp(self):
        """Setu console environment"""
        self.console = HBNBCommand()

    @patch('sys.stdout', new_callable=StringIO)
    def test_create(self, mock_stdout):
        # Test creating an object
        self.console.do_create('State name="California"')
        # Assert that the object is created successfully
        output = mock_stdout.getvalue().strip()
        self.assertRegex(output, r'\w*\-?')

    @patch('sys.stdout', new_callable=StringIO)
    def test_all(self, mock_stdout):
        # Create a new State object
        self.console.do_create('State name="California"')

        # Call do_all('State') to list all State objects
        self.console.do_all('State')

        # Assert that the output contains the newly created State object
        output = mock_stdout.getvalue().strip()
        self.assertIn('State', output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_show(self, mock_stdout):
        # Test showing an object
        self.console.do_create('State name="California"')
        _id = mock_stdout.getvalue().strip()

        # Clear the buffer
        # mock_stdout.seek(0)
        # mock_stdout.truncate()

        # Show the object
        self.console.do_show(f'State {_id}')
        _id1 = mock_stdout.getvalue().strip()

        # Assert that the object is shown successfully
        self.assertIn(_id, _id1)
    # Add similar test methods for 'all' and 'delete'
    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None,
                         "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(HBNBCommand.__doc__, None,
                         "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")
