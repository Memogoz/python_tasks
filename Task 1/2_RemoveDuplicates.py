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
    input_list = ast.literal_eval(sys.argv[1]) 
    # Check if it's a list of integers
    if not isinstance(input_list, list) or not all(isinstance(i, int) for i in input_list):
        raise ValueError
except:
    print('Invalid list format. Format should be "[<int>, <int>, <int>, ...]"')
    sys.exit(1)

# Remove duplicates and create tuple
unique_tuple = tuple(set(input_list))

# Print results
print(f"List:  {input_list}")  
print(f"Tuple: {unique_tuple}")
print(f"Min: {min(unique_tuple)}")
print(f"Max: {max(unique_tuple)}")
