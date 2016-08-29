#!/usr/local/bin/python3
import gnupg
import sys
import os.path
import glob
import argparse
import json

BINARY = '/usr/local/bin/gpg'
GPG_DIR = '~/.gnupg/'
FILE = 'secrets'

gpg=gnupg.GPG(binary=BINARY,homedir=GPG_DIR)

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
	file = open_read_file(FILE)
	return  gpg.decrypt(file.read())

def update_keys():
	encrypt_content(str(decrypt_content()))

def get_key_value(id, option):
	json_content = json.loads(str(decrypt_content()))
	if option.lower() == 'all': print('Key:',json_content[id][0],'\nValue:',json_content[id][1])
	if option.lower() == 'key': print(json_content[id][0])
	if option.lower() == 'value': print(json_content[id][1])

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
	output = input('Copy Key (k) or Value (v) to clipboard? (N/k/v): ' )
	if output.lower() == 'k': os.system("echo '{}' | pbcopy".format(json_content[id][0]))
	if output.lower() == 'v': os.system("echo '{}' | pbcopy".format(json_content[id][1]))
	output = input('Show key/value pair? (N/y): ' )
	if output.lower() == 'y': print('Key:',json_content[id][0],'\nValue:',json_content[id][1])

def add_content(id, key, value, json_content):
	json_content[id] = [key, value]
	jkv = json.dumps(json_content, sort_keys=True)
	encrypt_content(jkv)

def modify_content():
	id = id_or_list()
	json_content = json.loads(str(decrypt_content()))
	json_content.pop(id, None)

	print("Leave key/value without values for delete")
	key = input("Introduce a key: ")
	value = input("Introduce a value: ")

	if key != '' and value != '':
		add_content(id, key, value, json_content)
		print("Done! Identifier " + id +" has been modified")
	else:
		jkv = json.dumps(json_content, sort_keys=True)
		encrypt_content(jkv)
		print("Done! Identifier " + id +" has been deleted")

def open_read_file(file):
	file = open('secrets', 'a+')
	file.seek(0)
	return file

def write_in_file(file, content):
	file.write(content)
	file.close()

def show_keys():
	json_content = json.loads(str(decrypt_content()))
	for key in sorted(json_content.keys()):
		print(key)

def initialize():
	file  = open('secrets', 'w+')
	id = input('Introduce an Identifier: ').replace(' ','_')
	key = input('Introduce a Key: ')
	value = input('Introduce a Value: ')
	jkv = json.dumps({id : [ key , value ]}, sort_keys=True)
	encrypt_content(jkv)

def add_menu():
	file  = open('secrets', 'a+')
	json_content = json.loads(str(decrypt_content()))

	id = input('Please Introduce an Identifier: ').replace(' ','_')
	while (id in json_content):
		id = input('This identifier exist. Please Introduce other Identifier: ').replace(' ','_')

	key = input('Introduce a Key: ')
	value = input('Introduce a Value: ')
	add_content(id, key, value, json_content)

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
		option = int(input('\t1: Add Key/Value Pair\n\t2: Modify/Delete Key/Value Pair\n\t3: Decrypt Key/Value Pair\n\t4: Show Keys\n\t5: Update public keys\n\t6: Exit\nChoose: '))
		while option not in range(1, len(switcher)):
			option = int(input('Choose correct option: ' ))

		func = switcher.get(option, lambda: 'nothing')
		return func()
	else:
		print('The file', FILE,'has not been found, using -i/--interactive argument.')
		switcher = {
			0: lambda: '',
        		1: initialize,
        		2: exit
    		}
		option = int(input('\t1: Add Key/Value Pair\n\t2: Exit\nChoose: '))
		while option not in range(1, len(switcher)):
			option = int(input('Choose correct option: ' ))

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
	parser.add_argument("-a","--all", metavar='identifier', help="display the key and value pair for the given identifier")
	args = parser.parse_args()
	if args.interactive: interactive_menu()
	elif args.list: show_keys()
	elif args.key: get_key_value(args.key, 'key')
	elif args.value: get_key_value(args.value, 'value')
	elif args.all: get_key_value(args.all, 'all')
	elif not os.path.isfile(FILE): interactive_menu()
	else: parser.print_help()

if __name__ == "__main__":
	main(sys.argv[1:])
