#!/usr/bin/env python3
# Script that obtains system info from a Linux system

import argparse
import subprocess

parser = argparse.ArgumentParser(prog="5_SysInfo.py",
                                 description="Get general system information.")
parser.add_argument('-d', '--distro', action='store_true', help='Get Linux distribution information')
parser.add_argument('-m', '--memory', action='store_true', help='Get memory information')
parser.add_argument('-c', '--cpu', action='store_true', help='Get CPU information')
parser.add_argument('-u', '--user', action='store_true', help='Get user information')
parser.add_argument('-l', '--load', action='store_true', help='Get load average')
parser.add_argument('-i', '--ip', action='store_true', help='Get IP address')
args = parser.parse_args()

# Check if no arguments are provided
if not any(vars(args).values()):
    parser.print_help()
    exit(1)

# Print selected values
if args.distro:
    distroInfo = subprocess.check_output('cat /etc/os-release | grep -E "^NAME=" && cat /etc/os-release | grep -E "^VERSION="', shell=True, text=True)
    print(f'=== DISTRIBUTION INFO ===\n{distroInfo}')
if args.memory:
    memoryInfo = subprocess.check_output('free -h', shell=True, text=True)
    print(f'=== MEMORY INFO ===\n{memoryInfo}')
if args.cpu:
    cpuInfo = subprocess.check_output('cat /proc/cpuinfo | grep -E "model name|processor|cpu MHz"', shell=True, text=True)
    print(f'=== CPU INFO ===\n{cpuInfo}')
if args.user:
    userInfo = subprocess.check_output('whoami', shell=True, text=True)
    print(f'=== USER NAME ===\n{userInfo}')
if args.load:
    loadAvg = subprocess.check_output('uptime', shell=True, text=True)
    print(f'=== LOAD AVERAGE ===\n{loadAvg}')
if args.ip:
    ipAddr = subprocess.check_output('hostname -I', shell=True, text=True)
    print(f'=== IP ADRESS ===\n{ipAddr}')