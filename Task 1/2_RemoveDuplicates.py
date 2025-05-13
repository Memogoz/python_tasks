#!/usr/bin/env python3
# Script to remove duplicates from a list, create a tuple, and find the max and min values

import sys
import ast

# Check number of arguments
if len(sys.argv) != 2:
    print('Usage: ./2_RemoveDuplicates.py "[<list>]"')
    sys.exit(1)

# Convert argument to list
try:
    list = ast.literal_eval(sys.argv[1]) 
    # Check if its a list of integers
    if not isinstance(list, list) or not all(isinstance(i, int) for i in list):
        raise ValueError
except:
    print('Invalid list format. Format should be "[<int>, <int>, <int>, ...]"')
    sys.exit(1)

# Remove duplicates and create tuple
tuple = tuple(set(list))

# Print results
print(f"List:  {list}")  
print(f"Tuple: {tuple}")
print(f"Min: {min(tuple)}")
print(f"Max: {max(tuple)}")
