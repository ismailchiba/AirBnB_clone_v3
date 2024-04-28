#!/usr/bin/python3
"""
This script checks for missing docstrings in Python
classes and functions within a specified directory.
It recursively traverses the directory, examining
each Python file for modules, classes, and functions
that lack a docstring and reports the findings.
"""

import ast
import os
import subprocess


class DocStringChecker(ast.NodeVisitor):
    """
    A class that extends ast.NodeVisitor to check for docstrings
    in Python class and function definitions.
    Attributes:
        undocumented (list): A list to store the names
        of undocumented Python entities.
    """

    def __init__(self):
        "init functio"
        self.undocumented = (
            []
        )  # Initialize the list to hold undocumented entities

    def visit_Module(self, node):
        """
        Visit a module node in the AST and check for a docstring.

        Args:
            node (ast.Module): The module node to check.
        """
        if not ast.get_docstring(node):
            self.undocumented.append(
                ("module", node)
            )  # Append to undocumented if no docstring
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_ClassDef(self, node):
        """
        Visit a class definition node in the AST and check for a docstring.

        Args:
            node (ast.ClassDef): The class definition node to check.
        """
        if not ast.get_docstring(node):
            self.undocumented.append(
                ("class", node.name)
            )  # Append to undocumented if no docstring
        self.generic_visit(node)  # Continue visiting child nodes

    def visit_FunctionDef(self, node):
        """
        Visit a function definition node in the AST and check for a docstring.

        Args:
            node (ast.FunctionDef): The function definition node to check.
        """
        if not ast.get_docstring(node):
            self.undocumented.append(
                ("function", node.name)
            )  # Append to undocumented if no docstring
        self.generic_visit(node)  # Continue visiting child nodes


def check_documentation(file_path):
    """
    Check a Python file for undocumented classes and functions.

    Args:
        file_path (str): The path to the Python file to check.

    Returns:
        list: A list of undocumented entities in the file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        node = ast.parse(
            file.read(), filename=file_path
        )  # Parse the file content to an AST
    checker = DocStringChecker()  # Create an instance of DocStringChecker
    checker.visit(node)  # Visit the AST nodes
    return checker.undocumented  # Return the list of undocumented entities


def check_pycodestyle(file_path):
    """
    Check a Python file for PEP8 compliance using pycodestyle.

    Args:
        file_path (str): The path to the Python file to check.

    Returns:
        str: The output from the pycodestyle check.
    """
    result = subprocess.run(
        ["pycodestyle", "--first", file_path], capture_output=True, text=True
    )
    return result.stdout


def format_with_black(file_path):
    """
    Format a Python file using the black formatter.

    Args:
        file_path (str): The path to the Python file to format.
    """
    subprocess.run(["black", "--line-length", "79", file_path])


if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.realpath(__file__))
    total_files = 0
    total_documented = 0
    total_undocumented = 0

    for root, dirs, files in os.walk(root_directory):
        for file in files:
            if "site-packages" in root or "venv" in root:
                continue
            if file.endswith(".py") and file != "__init__.py":
                total_files += 1
                file_path = os.path.join(root, file)
                undocumented = check_documentation(file_path)
                if undocumented:
                    total_undocumented += 1
                    print(f"Undocumented entities in {file}:")
                # Run pycodestyle check
                pycodestyle_output = check_pycodestyle(file_path)
                if pycodestyle_output:
                    print(f"PEP8 issues in {file}:\n{pycodestyle_output}")
                # Format file with black
                format_with_black(file_path)

    # Print the summary of documentation check
    print(f"\nTotal files checked: {total_files}")
    print(f"Total documented files: {total_documented}")
    print(f"Total undocumented files: {total_undocumented}")
