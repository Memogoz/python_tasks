#!/usr/bin/env python3 
# Script to analyze a logs and provide stadistics on User Agents

import sys
import re
from collections import Counter

# Check number of arguments
if len(sys.argv) != 2:
    print("Usage: ./3_LogAnalisis.py <filename>")
    sys.exit(1)

file = sys.argv[1]

# Check if file exists
try:
    with open(file, 'r') as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"File {file} not found.")
    sys.exit(1)
except Exception as e:
    print(f"Error reading file {file}: {e}")
    sys.exit(1)

# Check if file is empty
if not lines:
    print(f"File {file} is empty.")
    sys.exit(1)

# Count user agents with Counter
user_agents = Counter()
for line in lines:
    match = re.search(r'"([^"]*)"$', line.strip()) 
    if match:
        user_agents[match.group(1)] += 1

# Print result analiisis
for ua, count in user_agents.items():
    print(f"{count} request(s) by : {ua}")
