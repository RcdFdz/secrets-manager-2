import json
import os
import sys
import pyperclip
import platform
from collections import OrderedDict
from command_controler import CommandControler
from gpg_tools import GPGTools

KEYS = OrderedDict([('user', None), ('password', None), ('url', None), ('other', None)])

class InteractiveCMD:
	cmdc = ''
	FILE = ''

	def __init__(self, gpg):
		self.cmdc = CommandControler(gpg)
		self.FILE = gpg.get_file()

	def id_or_list(self):
		keys_list = self.cmdc.get_keys()
		id = raw_input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
		while id.lower()=='list' or id not in keys_list:
			if id.lower()=='list' :
				self.show_keys()
				id = raw_input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
			if id not in keys_list:
				id = raw_input("Introduce a valid identifier name or 'list' for list all identifiers: ").replace(' ','_')
		return id

	def add_content(self):
		id = raw_input('Please Introduce an Identifier: ').replace(' ','_')
		if(os.path.isfile(self.FILE)):
			while(id in self.cmdc.get_keys()):
				id = raw_input('Please Introduce an Identifier: ').replace(' ','_')

		for el in KEYS:
			KEYS[el] = raw_input("Please introduce a value for '" + str(el.lower()) + "' field, or leave it empty: ")
		new_json_content = {id:dict(KEYS)}
		self.cmdc.add_content(json.dumps(new_json_content))

	def modify_content(self):
		id = self.id_or_list()
		json_content = json.loads(self.cmdc.get_json())
		json_content.pop(id, None)
		new_json = {}
		print('Leave all elements without value for delete the entry')

		for e in KEYS:
			element = raw_input('New ' + str(e) + ': ')
			new_json[e] = element

		if all( values == '' for key, values in new_json.items()):
			jkv = json.dumps(json_content, sort_keys=True)
			self.cmdc.set_json(jkv)
			print('Done! Identifier ' + id + ' has been deleted')
		else:
			json_content[id] = new_json
			jkv = json.dumps(json_content, sort_keys=True)
			self.cmdc.set_json(jkv)
			print('Done! Identifier ' + id + ' has been modified')

	def show_keys(self):
		self.cmdc.show_keys()

	def update_keys(self):
		self.cmdc.update_keys()

	def print_decrypt_content(self):
		id = self.id_or_list()
		json_content = json.loads(self.cmdc.get_json())

		output = raw_input('Show values? (Y/n): ')
		while output.lower() != 'y' and output.lower() != 'n' and output.lower() != 'yes' and output.lower() != 'no' and output.lower() != '':
			output = raw_input('Show values? (Y/n): ')

		if output.lower() == '' or output.lower() == 'y' or output.lower() == 'yes':
			for e in KEYS:
				print(str(e) + ': ' + str(json_content[id][e]))

		output = raw_input('Copy any elemento to clipboard? (N/element name): ' )
		while output.lower() not in KEYS and output.lower() != '' and output.lower() != 'n' and output.lower() != 'no':
				output = raw_input("Please choose 'no' for leave. For copy and element 'user', 'password', 'url' or 'other': " )

		if output.lower() != '' and  output.lower() != 'no' and output.lower() != 'n':
			if platform.system() == 'Darwin':
				pyperclip.copy(json_content[id][output.lower()])
			else:
				print('Only Darwin platforms')

	def exit(self):
		sys.exit(0)

	def raw_input_menu(self, option, switcher):
		while True:
			try:
				option = int(option)
				if option not in range(1,switcher): raise ValueError
				break
			except:
				option = raw_input('Please, choose correct option: ')
		return option

	def interactive_menu(self):
		if os.path.isfile(self.FILE):
			switcher = {
				0: lambda: '',
				1: self.add_content,
				2: self.modify_content,
				3: self.print_decrypt_content,
				4: self.show_keys,
				5: self.update_keys,
				6: self.exit
			}
			option = raw_input('\t1: Add Key/Value Pair\n\t2: Modify/Delete Key/Value Pair\n\t3: Decrypt Key/Value Pair\n\t4: Show Keys\n\t5: Update public keys\n\t6: Exit\nChoose: ')
			option = self.raw_input_menu(option, len(switcher))
			func = switcher.get(option, lambda: 'nothing')
			return func()
		else:
			print('The file' + self.FILE + 'has not been found, using -i/--interactive argument.')
			switcher = {
				0: lambda:'',
				1: self.add_content,
				2: self.exit
			}
			option = raw_input('\t1: Add\n\t2: Exit\nChoose: ')
			option = self.raw_input_menu(option, len(switcher))
			func = switcher.get(option, lambda: 'nothing')
			return func()

	def main(self):
		pass

if __name__ == '__main__':
	gpg = GPGTools()
	icmd = InteractiveCMD(gpg)
	icmd.main()
