import json
import os
import sys
from collections import OrderedDict
from gpg_tools import GPGTools
from json_manager import JSONManager
from command_controler import CommandControler

KEYS = OrderedDict([('user', None), ('password', None), ('url', None), ('other', None)])

class InteractiveCMD:
	gpg = ''
	cmdc = ""

	def __init__(self, gpg):
		self.gpg = gpg
		self.cmdc = CommandControler(gpg)

	def add_content(self):
		id = input('Please Introduce an Identifier: ').replace(' ','_')
		for el in KEYS:
			KEYS[el] = input("Please introduce a value for '" + str(el.lower()) + "' field, or leave it empty: ")
		self.jm.add(id, KEYS)

	def add_menu(self):
		return(0)

	def modify_content(self):
		return(0)

	def show_keys(self):
		cmdc.show_keys(gpg)

	def print_decrypt_content(self):
		return(0)

	def exit(self):
		sys.exit(0)

	def input_menu(self, dummy):
		return(0)

	def initialize(self):
		return(0)

	def interactive_menu(self):
		if os.path.isfile(FILE):
			switcher = {
				0: lambda: '',
				1: self.add_menu,
				2: self.modify_content,
				3: self.print_decrypt_content,
				4: self.show_keys,
				5: self.update_keys,
				6: self.exit
			}
			option = input('\t1: Add Key/Value Pair\n\t2: Modify/Delete Key/Value Pair\n\t3: Decrypt Key/Value Pair\n\t4: Show Keys\n\t5: Update public keys\n\t6: Exit\nChoose: ')
			func = switcher.get(option, lambda: 'nothing')
			return func()
		else:
			print('The file' + FILE + 'has not been found, using -i/--interactive argument.')
			switcher = {
				0: lambda: '',
				1: self.initialize,
				2: self.exit
			}
			option = input('\t1: Add\n\t2: Exit\nChoose: ')
			func = switcher.get(option, lambda: 'nothing')
			return func()

	def main(self):
		pass

if __name__ == '__main__':
	icmd = InteractiveCMD()
	icmd.main()
