#!/usr/bin/env python

import argparse
import socket
import sys

parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="The IP address of the SMTP server.")
parser.add_argument("--wordlist", help="Wordlist file of usernames to check.")
parser.parse_args()

with open(args.wordlist, "r") as wordList:
	words = [word.strip() for word in wordList]

#Establish the connection
print "[*] Attempting to connect to SMTP on %s..." % ip
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connect = s.connect((args.ip,25))
print "[+] Connected successfully to %s!\n" % ip

#Print the banner
print "[*] Getting banner..."
banner = s.recv(1024)
print "[+] BANNER: " + banner

#Set a cooldown count
zeroCool = 1

#See if each user exists, if so print them
for word in words:
	if zeroCool != 6:
		zeroCool += 1
		print "[*] Trying %s..." % word.lower()
		s.send('VRFY %s\r\n' % word.lower())
		result = s.recv(1024)
		if "250" in result:
			print "[!] USER FOUND: " + result.split(" ")[2].split("<")[1].split(">")[0]

	else:
		print "[!] Cooldown limit reached, resetting connection..."
		s.close()
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((args.ip,25))
		print "[+] Connection reset!"
		zeroCool = 1

#Close the connection
s.close()

print "[+] Task completed"
