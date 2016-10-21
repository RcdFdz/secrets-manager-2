#!/usr/local/bin/python3
import argparse
import os
from interactive_cmd import InteractiveCMD

FILE = 'secrets'

class Main:
	def main(argv):
		icmd = InteractiveCMD()
		parser = argparse.ArgumentParser(description='Manager for sensible information under PGP')
		parser.add_argument("-i","--interactive", help="display the interactive menu for pwd-manager",
			action="store_true")
		parser.add_argument("-l","--list", help="list all the stored identifiers", action="store_true")
		parser.add_argument("-k","--key", metavar='identifier', help="return the key for the given identifier")
		parser.add_argument("-v","--value", metavar='identifier', help="return the value for the given identifier")
		parser.add_argument("-e","--element", nargs=2, metavar=('identifier','element_number'), help="return the element number for the given identifier")
		parser.add_argument("-a","--all", metavar='identifier', help="display the key and value pair for the given identifier")
		args = parser.parse_args()
		if args.interactive: icmd.interactive_menu()
		elif args.list: show_keys()
		elif args.key: get_key_value(args.key, 'key')
		elif args.value: get_key_value(args.value, 'value')
		elif args.all: get_key_value(args.all, 'all')
		elif args.element: get_key_value(args.element, 'element')
		elif not os.path.isfile(FILE): interactive_menu()
		else: parser.print_help()

if __name__ == '__main__':
	m = Main();
	m.main()
