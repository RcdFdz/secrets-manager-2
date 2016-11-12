#!/usr/local/bin/python3
import argparse
import os
import sys
from interactive_cmd import InteractiveCMD
from gpg_tools import GPGTools

FILE = 'secrets'

class Main:

	def get_key_value(args, option):
		json_content = json.loads(str(decrypt_content()))
		if option.lower() == 'all':
			for e in KEYS:
				print(e.capitalize() + ': ' + json_content[args][e])
		elif option.lower() == 'user': print(json_content[args]['user'])
		elif option.lower() == 'pass': print(json_content[args]['password'])
		elif option.lower() == 'url': print(json_content[args]['url'])
		elif option.lower() == 'other': print(json_content[args]['other'])

	def main(argv):
		gpg = GPGTools(file=FILE)
		icmd = InteractiveCMD(gpg)
		parser = argparse.ArgumentParser(description='Manager for sensible information under PGP')
		parser.add_argument('-i','--interactive', help='display the interactive menu for pwd-manager',
			action='store_true')
		parser.add_argument('-l','--list', help='list all the stored identifiers', action='store_true')
		parser.add_argument('-u','--user', metavar='identifier', help='return the username for the given identifier')
		parser.add_argument('-p','--password', metavar='identifier', help='return the password for the given identifier')
		parser.add_argument('-ur','--url', metavar='identifier', help='return the URL for the given identifier')
		parser.add_argument('-o','--other', metavar='identifier', help='return the other for the given identifier')
		parser.add_argument('-a','--all', metavar='identifier', help='display all values for the given identifier')
		args = parser.parse_args()
		if args.interactive: interactive_menu()
		elif args.list: show_keys()
		elif args.user: get_key_value(args.user, 'user')
		elif args.password: get_key_value(args.password, 'pass')
		elif args.url: get_key_value(args.url, 'url')
		elif args.other: get_key_value(args.other, 'other')
		elif args.all: get_key_value(args.all, 'all')
		elif not os.path.isfile(FILE): interactive_menu()
		else: parser.print_help(

if __name__ == '__main__':
	m = Main();
	m.main(sys.argv[1:])
