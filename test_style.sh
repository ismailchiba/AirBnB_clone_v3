#!/usr/bin/env bash

find . -type f -name "*.py" | while read -r file_path; do
    flake8 "$file_path"
done