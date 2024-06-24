#!/usr/bin/env python3
import os
import subprocess


def check_pycodestyle(directory):
    """
    Check for PEP8compliance using pycodestyle in the given directory.
    Args:
        directory (str): The root directory to start checking from.
    """
    # Define the directories to exclude from checking
    excluded_dirs = {"venv", "site-packages"}

    # Walk through the directory tree
    for root, dirs, files in os.walk(directory, topdown=True):
        # Modify dirs in-place to skip excluded directories
        dirs[:] = [d for d in dirs if d not in excluded_dirs]

        for file in files:
            if file.endswith(".py"):
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Run pycodestyle check
                result = subprocess.run(
                    ["pycodestyle", file_path], capture_output=True, text=True
                )
                if result.stdout:
                    # If there are PEP8 issues, print them out
                    print(
                        "PEP8 issues in {}:\n{}".format(
                            file_path, result.stdout
                        )
                    )


if __name__ == "__main__":
    # Get the current working directory as the starting point
    project_directory = os.getcwd()
    # Run the PEP8 compliance check
    check_pycodestyle(project_directory)
