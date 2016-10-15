import json
import os
from collections import OrderedDict

KEYS = OrderedDict([('user', None), ('password', None), ('url', None), ('other', None)])

class InteractiveCMD:
	def id_or_list():
		json_content = json.loads(str(decrypt_content()))
		id = input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
		while id.lower()=='list' or id not in json_content:
			if id.lower()=='list' :
				show_keys()
				id = input("Introduce the identifier name or 'list' for list all identifiers: ").replace(' ','_')
			if id not in json_content:
				id = input("Introduce a valid identifier name or 'list' for list all identifiers: ").replace(' ','_')
		return id

	def print_decrypt_content():
		id = id_or_list()
		json_content = json.loads(str(decrypt_content()))

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
	def input_menu(option, switcher):
	while True:
		try:
			option = int(option)
			if option not in range(1,switcher): raise ValueError
			break
		except:
			option = input('Please, choose correct option: ')
	return option

	def add_menu():
		file  = open('secrets', 'a+')
		json_content = json.loads(str(decrypt_content()))

		id = input('Please Introduce an Identifier: ').replace(' ','_')
		while (id in json_content):
			id = input('This identifier exist. Please Introduce other Identifier: ').replace(' ','_')
		json_content = add_content(id, json_content)

	def initialize():
		id = input('Please Introduce an Identifier: ').replace(' ','_')
		add_content(id)

	def modify_content():
		self.id_or_list()
		print('Leave all elements without value for delete the entry')

	def interactive_menu():
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
			option = input_menu(option, len(switcher))
			func = switcher.get(option, lambda: 'nothing')
			return func()
		else:
			print('The file' + FILE + 'has not been found, using -i/--interactive argument.')
			switcher = {
				0: lambda: '',
				1: initialize,
				2: exit
			}
			option = input('\t1: Add\n\t2: Exit\nChoose: ')
			option = input_menu(option, len(switcher))
			func = switcher.get(option, lambda: 'nothing')
			return func()
