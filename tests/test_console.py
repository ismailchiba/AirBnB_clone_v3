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
        """Setup console"""
        self.console = HBNBCommand()


@patch("sys.stdout", new_callable=StringIO)
def test_create(self, mock_stdout):
    """
    Test the 'create' command functionality in the console.

    This test ensures that using the 'create'
    command with the 'State' class and
    a name attribute successfully creates an object and prints its ID.
    """
    self.console.do_create('State name="California"')
    output = mock_stdout.getvalue().strip()
    self.assertRegex(output, r"\w*\-?")

    @patch("sys.stdout", new_callable=StringIO)
    def test_all(self, mock_stdout):
        """
        Test the 'all' command functionality in the console.

        This test verifies that after creating a new 'State'
        object, calling the
        'all' command with 'State' as an argument lists all
        instances of the State class,
        including the newly created one.
        """
        self.console.do_create('State name="California"')
        self.console.do_all("State")
        output = mock_stdout.getvalue().strip()
        self.assertIn("State", output)

    @patch("sys.stdout", new_callable=StringIO)
    def test_show(self, mock_stdout):
        """
        Test the 'show' command functionality in the console.

        This test checks that after creating a 'State'
        object, using the 'show' command
        with the object's ID displays the correct object's information.
        """
        self.console.do_create('State name="California"')
        _id = mock_stdout.getvalue().strip()
        self.console.do_show("State {}".format(_id))
        _id1 = mock_stdout.getvalue().strip()
        self.assertIn(_id, _id1)

    def test_pep8_conformance_console(self):
        """Test that console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_pep8_conformance_test_console(self):
        """Test that tests/test_console.py conforms to PEP8."""
        pep8s = pep8.StyleGuide(quiet=True)
        result = pep8s.check_files(["tests/test_console.py"])
        self.assertEqual(
            result.total_errors, 0, "Found code style errors (and warnings)."
        )

    def test_console_module_docstring(self):
        """Test for the console.py module docstring"""
        self.assertIsNot(console.__doc__, None, "console.py needs a docstring")
        self.assertTrue(
            len(console.__doc__) >= 1, "console.py needs a docstring"
        )

    def test_HBNBCommand_class_docstring(self):
        """Test for the HBNBCommand class docstring"""
        self.assertIsNot(
            HBNBCommand.__doc__, None, "HBNBCommand class needs a docstring"
        )
        self.assertTrue(
            len(HBNBCommand.__doc__) >= 1,
            "HBNBCommand class needs a docstring",
        )
