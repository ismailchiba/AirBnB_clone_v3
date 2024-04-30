#!/bin/bash

# Function to check for non-executable files
check_non_executable_files() {
    root_dir="$1"
    find "$root_dir" -type f ! -executable
}

# Function to print paths relative to the root directory
print_paths_from_root() {
    root_dir="$1"
    while IFS= read -r filepath; do
        relative_path="${filepath#$root_dir/}"
        echo "$relative_path"
    done
}

# Main script
root_dir="$1"

if [ -z "$root_dir" ]; then
    echo "Usage: $0 <root_directory>"
    exit 1
fi

# Use a while loop to read each line output from the check_non_executable_files function
check_non_executable_files "$root_dir" | while IFS= read -r file; do
    if [ -n "$file" ]; then
        echo "Non-executable file found:"
        print_paths_from_root "$root_dir" <<< "$file"
    else
        echo "No non-executable files found."
    fi
done
