#!/usr/bin/python3
"""cript to check documentatios"""
import ast
import os

def is_documented(node):
    """Check if the node has a docstring."""
    return bool(ast.get_docstring(node))

def check_documentation(file_path, undocumented_files):
    """Check the documentation of Python file."""
    documented = True
    with open(file_path, 'r', encoding='utf-8') as file:
        node = ast.parse(file.read(), filename=file_path)
    
    # Check module docstring
    if not is_documented(node):
        documented = False
        undocumented_files.append((file_path, 'module'))
    
    # Check classes and functions
    for item in node.body:
        if isinstance(item, ast.ClassDef) and not is_documented(item):
            documented = False
            undocumented_files.append((file_path, f'class {item.name}'))
        elif isinstance(item, ast.FunctionDef) and not is_documented(item):
            documented = False
            undocumented_files.append((file_path, f'function {item.name}'))
    
    return documented

def test_all_py_files(root_dir):
    """Walk through the directory and check all Python files."""
    total_files = 0
    undocumented_files = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                total_files += 1
                file_path = os.path.join(root, file)
                if not check_documentation(file_path, undocumented_files):
                    print(f"NOT DOCUMENTED: {file_path}")
    
    # Summary of results
    print(f"\nTotal files checked: {total_files}")
    print(f"Number of undocumented files: {len(undocumented_files)}")
    if undocumented_files:
        print("Undocumented files and their paths:")
        for file_path, entity in undocumented_files:
            print(f"{entity} in {file_path}")

if __name__ == "__main__":
    root_directory = os.path.dirname(os.path.realpath(__file__))
    test_all_py_files(root_directory)
