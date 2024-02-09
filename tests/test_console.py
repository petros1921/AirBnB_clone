#!/usr/bin/python3
"""Defines unittests for console.py.

Unittest classes:
    TestHBNBCommandPrompting
    TestHBNBCommandHelp
    TestHBNBCommandExit
    TestHBNBCommandCreate
    TestHBNBCommandShow
    TestHBNBCommandAll
    TestHBNBCommandDestroy
    TestHBNBCommandUpdate
"""
import os
import sys
import unittest
from models import storage
from models.engine.file_storage import FileStorage
from console import HBNBCommand
from io import StringIO
from unittest.mock import patch


class TestHBNBCommandPrompting(unittest.TestCase):
    """Unittests for testing prompting of the HBNB command interpreter."""

    def test_prompt_string(self):
        self.assertEqual("(HBNB) ", HBNBCommand.prompt)

    def test_empty_line(self):
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd(""))
            self.assertEqual("", output.getvalue().strip())

class TestHBNBCommandHelp(unittest.TestCase):
    """Unittests for testing help messages of the HBNB command interpreter."""

    def test_help_quit(self):
        expected_help_message = "Command to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help quit"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_create(self):
        expected_help_message = (
            "Usage: create <class>\n"
            "Create a new instance of a class and print its ID."
        )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help create"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_EOF(self):
        expected_help_message = "Signal to exit the program."
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help EOF"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_show(self):
    expected_help_message = (
        "Usage: show <class> <id> or <class>.show(<id>)\n"
        "Display the string representation of a class instance of a given id."
    )
    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("help show"))
        self.assertEqual(expected_help_message, output.getvalue().strip())
    
    def test_help_destroy(self):
        expected_help_message = (
                "Usage: destroy <class> <id> or <class>.destroy(<id>)\n"
                "Delete a class instance of a given id."
                )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help destroy"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_all(self):
        expected_help_message = (
                "Usage: all or all <class> or <class>.all()\n"
                "Display string representations of all instances of a given class.\n"
                "If no class is specified, displays all instantiated objects."
                )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help all"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_count(self):
    expected_help_message = (
        "Usage: count <class> or <class>.count()\n"
        "Retrieve the number of instances of a given class."
    )
    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("help count"))
        self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help_update(self):
        expected_help_message = (
                "Usage: update <class> <id> <attribute_name> <attribute_value> or\n"
                "       <class>.update(<id>, <attribute_name>, <attribute_value>) or\n"
                "       <class>.update(<id>, <dictionary>)\n"
                "Update a class instance of a given id by adding or updating\n"
                "a given attribute key/value pair or dictionary."
                )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help update"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

    def test_help(self):
        expected_help_message = (
                "Documented commands (type help <topic>):\n"
                "========================================\n"
                "EOF  all  count  create  destroy  help  quit  show  update"
                )
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("help"))
            self.assertEqual(expected_help_message, output.getvalue().strip())

class TestHBNBCommandExit(unittest.TestCase):
    """Unittests for testing exiting from the HBNB command interpreter."""

    def test_quit_exits(self):
        # Verify that the 'quit' command exits the program
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("quit"))

    def test_EOF_exits(self):
        # Verify that the 'EOF' command exits the program
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertTrue(HBNBCommand().onecmd("EOF"))


class TestHBNBCommandCreate(unittest.TestCase):
    """Unittests for testing create from the HBNB command interpreter."""

    @classmethod
    def setUp(self):
        # Set up the test environment
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    @classmethod
    def tearDown(self):
        # Tear down the test environment
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_create_missing_class(self):
        # Verify the output when the class name is missing
        expected_output = "** class name missing **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_invalid_class(self):
        # Verify the output when the class doesn't exist
        expected_output = "** class doesn't exist **"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("create MyModel"))
            self.assertEqual(expected_output, output.getvalue().strip())

    def test_create_invalid_syntax(self):
        # Verify the output when the syntax is unknown
        expected_output = "*** Unknown syntax: MyModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("MyModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())
        expected_output = "*** Unknown syntax: BaseModel.create()"
        with patch("sys.stdout", new=StringIO()) as output:
            self.assertFalse(HBNBCommand().onecmd("BaseModel.create()"))
            self.assertEqual(expected_output, output.getvalue().strip())

def test_create_object(self):
    # Verify that objects are created successfully
    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create BaseModel"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "BaseModel.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create User"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "User.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create State"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "State.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create City"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "City.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create Amenity"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "Amenity.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create Place"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "Place.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())

    with patch("sys.stdout", new=StringIO()) as output:
        self.assertFalse(HBNBCommand().onecmd("create Review"))
        self.assertLess(0, len(output.getvalue().strip()))
        test_key = "Review.{}".format(output.getvalue().strip())
        self.assertIn(test_key, storage.all().keys())
