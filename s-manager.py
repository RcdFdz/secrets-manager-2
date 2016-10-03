#!/usr/local/bin/python3
import gnupg
import sys
import os.path
import glob
import argparse
import json
import textwrap

BINARY = '/usr/local/bin/gpg'
GPG_DIR = '~/.gnupg/'
FILE = 'secrets'
KEYS = {'1. User' : None, '2. Password' : None, '3. Url' : None, '4. Other' : None}
gpg=gnupg.GPG(binary=BINARY,homedir=GPG_DIR)

def get_sentences(id):
	size = len(KEY_NAME_ORDER)
	if id >= size:
		sentence = 'Element ' + str(id+1)
	else:
		sentence = KEY_NAME_ORDER[id]
	return sentence

def get_keys():
	files = glob.glob('./pub-keys/*.asc')
	keys_data = ''
	for name in files:
		try:
			with open(name) as file:
				 keys_data+=str(file.read())
		except IOError as exc:
			if exc.errno != errno.EISDIR: # Do not fail if a directory is found, just ignore it.
				raise # Propagate other kinds of IOError.
	import_result = gpg.import_keys(keys_data)
	fprints=[]
	for key in import_result.results:
		fprints.append(str(key['fingerprint']))
	return fprints

def encrypt_content(json_content):
	finger_prints = get_keys()
	return gpg.encrypt(json_content, *finger_prints, always_trust=True, output=FILE)

def decrypt_content():
	file = open(FILE, 'a+')
	file.seek(0)
	return gpg.decrypt(file.read())

def update_keys():
	encrypt_content(str(decrypt_content()))

def get_key_value(args, option):
	json_content = json.loads(str(decrypt_content()))
	if option.lower() == 'all':
		for elem in json_content[args]:
			print(elem)
	elif option.lower() == 'element': print(json_content[args[0]][int(args[1])-1])
	elif option.lower() == 'key': print(json_content[args][0])
	elif option.lower() == 'value': print(json_content[args][1])

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
	size = len(json_content[id])

	output = input('Show values? (Y/n): ' )
	if output.lower() == '' or output.lower() == 'y' or output.lower() == 'yes':
		for e in sorted(json_content[id].keys()):
			print(str(e) + ': ' + str(json_content[id][e]))

	output = input('Copy any elemento to clipboard? (N/element name): ' )
	while check_keys(output) and output.lower() != '' and output.lower() != 'n' and output.lower() and 'no':
		try:
				os.system("echo '{}' | pbcopy".format(json_content[id][output.lower()]))
		except KeyError:
			output = input('Please choose "user", "password", "url" or "note": ' )
			if check_keys(output):
				os.system("echo '{}' | pbcopy".format(json_content[id][output.lower()]))

def check_keys(output):
	exist = False
	for e in KEYS.keys():
		if output == e[3:]: exist = True
	return exist

def modify_content():
	id = id_or_list()
	json_content = json.loads(str(decrypt_content()))
	size = len(json_content[id])
	json_content.pop(id, None)

	print("Leave all elements without value for delete the entry")
	arr = []
	for e in range(0,size):
		element = input(get_sentences(e) + ': ')
		arr.append(element)

	if all(x == '' for x in arr):
		jkv = json.dumps(json_content, sort_keys=True)
		encrypt_content(jkv)
		print("Done! Identifier " + id +" has been deleted")
	else:
		json_content[id] = arr
		jkv = json.dumps(json_content, sort_keys=True)
		encrypt_content(jkv)
		print("Done! Identifier " + id +" has been modified")

def show_keys():
	json_content = json.loads(str(decrypt_content()))
	for key in sorted(json_content.keys()):
		print(key)

def add_content(id, old_content = None):
	json_content = {}

	for el in sorted(KEYS.keys()):
		KEYS[el] = input('Please introduce a value for "' + str(el.lower()[3:]) + '" field, or leave it empty: ')

	if old_content:
		old_content[id] = KEYS[el]
		json_content = old_content
	else:
		json_content[id] = KEYS

	jkv = json.dumps(json_content, sort_keys=True)
	encrypt_content(jkv)

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

def input_menu(option, switcher):
	while True:
		try:
			option = int(option)
			if option not in range(1,switcher): raise ValueError
			break
		except:
			option = input('Please, choose correct option: ')
	return option

def interactive_menu():
	if os.path.isfile(FILE):
		switcher = {
			0: lambda: '',
        		1: add_menu,
        		2: modify_content,
        		3: print_decrypt_content,
        		4: show_keys,
        		5: update_keys,
        		6: exit
    		}
		option = input('\t1: Add Key/Value Pair\n\t2: Modify/Delete Key/Value Pair\n\t3: Decrypt Key/Value Pair\n\t4: Show Keys\n\t5: Update public keys\n\t6: Exit\nChoose: ')
		option = input_menu(option, len(switcher))
		func = switcher.get(option, lambda: 'nothing')
		return func()

	else:
		print('The file', FILE,'has not been found, using -i/--interactive argument.')
		switcher = {
			0: lambda: '',
        		1: initialize,
        		2: exit
    		}
		option = input('\t1: Add\n\t2: Exit\nChoose: ')
		option = input_menu(option, len(switcher))
		func = switcher.get(option, lambda: 'nothing')
		return func()

def exit():
	sys.exit(0)

def main(argv):
	parser = argparse.ArgumentParser(description='Manager for sensible information under PGP')
	parser.add_argument("-i","--interactive", help="display the interactive menu for pwd-manager",
		action="store_true")
	parser.add_argument("-l","--list", help="list all the stored identifiers", action="store_true")
	parser.add_argument("-k","--key", metavar='identifier', help="return the key for the given identifier")
	parser.add_argument("-v","--value", metavar='identifier', help="return the value for the given identifier")
	parser.add_argument("-e","--element", nargs=2, metavar=('identifier','element_number'), help="return the element number for the given identifier")
	parser.add_argument("-a","--all", metavar='identifier', help="display the key and value pair for the given identifier")
	args = parser.parse_args()
	if args.interactive: interactive_menu()
	elif args.list: show_keys()
	elif args.key: get_key_value(args.key, 'key')
	elif args.value: get_key_value(args.value, 'value')
	elif args.all: get_key_value(args.all, 'all')
	elif args.element: get_key_value(args.element, 'element')
	elif not os.path.isfile(FILE): interactive_menu()
	else: parser.print_help()

if __name__ == "__main__":
	main(sys.argv[1:])
