#!/bin/bash

# curl -s https://api.github.com/repos/ideaguy3d/data-engineering-practice | grep size


# Set the size threshold in MB
SIZE_THRESHOLD_MB=1

# Convert MB to bytes (1 MB = 1048576 bytes)
SIZE_THRESHOLD_BYTES=$((SIZE_THRESHOLD_MB * 1048576))

# Find all files larger than the specified size
find . -type f -size +"$SIZE_THRESHOLD_BYTES"c -print | sed 's|^\./||' >> .gitignore

# Remove duplicate entries from .gitignore
sort -u .gitignore -o .gitignore

echo "Large files have been added to .gitignore and duplicates removed."

