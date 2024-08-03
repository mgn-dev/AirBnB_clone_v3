#!/usr/bin/python3
"""
Contains the class TestConsoleDocs
"""

import inspect
import unittest
import pycodestyle
from console import HBNBCommand
import console


class TestConsoleDocs(unittest.TestCase):
    """Class for testing documentation of the console"""

    def test_pep8_conformance_console(self) -> None:
        """Test that console.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_pep8_conformance_test_console(self) -> None:
        """Test that tests/test_console.py conforms to PEP8."""
        style = pycodestyle.StyleGuide(quiet=True)
        result = style.check_files(['tests/test_console.py'])
        self.assertEqual(result.total_errors, 0,
                         "Found code style errors (and warnings).")

    def test_console_module_docstring(self) -> None:
        """Test for the console.py module docstring"""
        self.assertIsNotNone(console.__doc__,
                             "console.py needs a docstring")
        self.assertTrue(len(console.__doc__) >= 1,
                        "console.py needs a docstring")

    def test_HBNBCommand_class_docstring(self) -> None:
        """Test for the HBNBCommand class docstring"""
        self.assertIsNotNone(HBNBCommand.__doc__,
                             "HBNBCommand class needs a docstring")
        self.assertTrue(len(HBNBCommand.__doc__) >= 1,
                        "HBNBCommand class needs a docstring")


if __name__ == "__main__":
    unittest.main()
