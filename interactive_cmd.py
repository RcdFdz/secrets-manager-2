import json
import os
import sys
from collections import OrderedDict
from json_manager import JSONManager
from command_controler import CommandControler

KEYS = OrderedDict([('user', None), ('password', None), ('url', None), ('other', None)])
FILE = 'secrets'

class InteractiveCMD:
	gpg = ''
	cmdc = ''

	def __init__(self, gpg):
		self.gpg = gpg
		self.cmdc = CommandControler(gpg)

	def id_or_list():
		keys_list = self.cmd.get_keys()
		id = input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
		while id.lower()=='list' or id not in keys_list:
			if id.lower()=='list' :
				self.show_keys()
				id = input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
			if id not in keys_list:
				id = input("Introduce a valid identifier name or 'list' for list all identifiers: ").replace(' ','_')
		return id

	def add_content(self):
		id = input('Please Introduce an Identifier: ').replace(' ','_')
		while(id in self.cmdc.get_keys()):
			id = input('Please Introduce an Identifier: ').replace(' ','_')

		for el in KEYS:
			KEYS[el] = input("Please introduce a value for '" + str(el.lower()) + "' field, or leave it empty: ")
		new_json_content = {id:dict(KEYS)}
		self.cmdc.add_content(new_json_content)

	def add_menu(self):
		return(0)

	def modify_content(self):
		return(0)

	def show_keys(self):
		self.cmdc.show_keys()

	def print_decrypt_content():
		id = id_or_list()
		json_content = json.loads(str(self.gpg.decrypt_content()))

		output = input('Show values? (Y/n): ')
		while output.lower() != 'y' and output.lower() != 'n' and output.lower() != 'yes' and output.lower() != 'no' and output.lower() != '':
			output = input('Show values? (Y/n): ')

		if output.lower() == '' or output.lower() == 'y' or output.lower() == 'yes':
			for e in KEYS:
				print(str(e) + ': ' + str(json_content[id][e]))

		output = input('Copy any elemento to clipboard? (N/element name): ' )
		while output.lower() not in KEYS and output.lower() != '' and output.lower() != 'n' and output.lower() != 'no':
			output = input("Please choose 'no' for leave. For copy and element 'user', 'password', 'url' or 'other': " )

		if output.lower() != '' and  output.lower() != 'no' and output.lower() != 'n':
			os.system("echo '{}' | pbcopy".format(json_content[id][output.lower()]))

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
