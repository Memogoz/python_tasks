#!/usr/bin/env python3
# Script to count the number of characters in a string

import sys
from collections import Counter

# Check number of arguments
if len(sys.argv) != 2:
    print("Usage: ./4_CharCount.py <string>")
    sys.exit(1)

# Asign string and remove blank spaces
string = sys.argv[1].strip()

#Count characters with Counter
char_count = Counter()
for char in string:
    char_count[char] += 1

# Print result 
for char, count in char_count.items():
    print(f"{char}:{count}", end=" ")


