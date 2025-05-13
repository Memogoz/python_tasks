#!/usr/bin/env python3
# Script to get the file extension from a file
import sys

# Check number of arguments
if len(sys.argv) != 2:
    print("Usage: ./1_FileExtension.py <filename>")
    sys.exit(1)

filename = sys.argv[1]

# Check if filename is valid
if "." not in filename :
    raise ValueError("Filename must contain at least one dot (.)")

# Get the file extension
file_extention = filename.split(".")[-1]

print(f"File extension: .{file_extention}")