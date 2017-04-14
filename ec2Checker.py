#!/usr/bin/env python

'''
Grant Page
CS 5651
Lab 4
Feb 22th 2016

This is a python script that will open a file and check the IP of the file to verify if it belongs to amazon ec2 if not it is printed out
'''

# Import Packages
import json
import socket
import errno
import re
import sys

# find_IPs Function - read over the JSON file and retunrn a list of IP addresses
def find_IPs():
    # Create an empty list
    IPs = []

    # Make a Regular Expression object that searches for IP addresses
    regex = re.compile(r'\d*\.\d*\.\d*\.\d*')

    try:
        # Open the JSON file with the python JSON library reader
        with open(sys.argv[1]) as json_data:
            # Load the JSON file
            data = json.load(json_data)

            # Search for IP addresses in the JSON data and make them a list
            IPs = regex.findall(str(data))

    except:
        # If there was an issue reading the JSON file. print and terminate
        print("ERROR: FILE NOT IN JSON FORMAT TERMINATING PROGRAM")
        exit(1)

    return IPs

# get_Host() - Get the Host Name for the ip address
def get_Host(ip_list):

    # Itterate through the IP list
    for (i,ip) in enumerate(ip_list):

        try:
            # Attempt to look-up the domain name
            host = socket.gethostbyaddr(ip)[0]

        except:
            # Default to "NOT FOUND"
            host = "NOT_FOUND"

        # Check for amazon EC2 address
        check_for_EC2(ip, host)

# check_for_EC2() - Get the Amazon EC2 address
def check_for_EC2(ip_addr, ip_name):

    # Make a Regular Expression
    regex_EC2 = re.compile(r'ec2-(.*)')

    # Search for EC2 Domain
    m_EC2 = regex_EC2.search(ip_name)

    # If Found then print it
    if m_EC2:
        print (ip_addr + "\t-> [+] " + ip_name)

# Main Function - look for IPs and test them using key functions
def main():
    if (len(sys.argv) != 2):
	print ("ERROR: ip-ranges.json must be the one and only argument.")
    else:
	# Check to see that the json file is the one and only argument
	if (sys.argv[1] != 'ip-ranges.json'):
	    # Print error statement
	    print ("ERROR: ip-ranges.json must be the one and only input file")
	else:
            # Create an empty list of IPs
            IPs = []
            IP_dict = {}

	    # Call the find_IPs function
            IPs = find_IPs()

            get_Host(IPs)

main()
