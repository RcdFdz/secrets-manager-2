import gnupg
import sys
import os.path
import glob
import argparse

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

def encrypt_content(content):
	finger_prints = get_keys()
	return gpg.encrypt(content, *finger_prints, always_trust=True, output=FILE)

def decrypt_content():
	file = open_read_file(FILE)
	return  gpg.decrypt(file.read())

def update_keys():
	encrypt_content(str(decrypt_content()))

def get_key_value(id, option):
	content = construct_dict()
	if option.lower() == 'all': print('Key: ',content[id][0],'\nValue: ',content[id][1])
	if option.lower() == 'key': print(content[id][0])
	if option.lower() == 'value': print(content[id][1])

def id_or_list():
	id = input("Introduce the identifier name or 'list' for list all identifiers: ")
	while id.lower()=='list' or not check_keys(id) :
		if id.lower()=='list' :
			show_keys()
			id = input("Introduce the identifier name or 'list' for list all identifiers: ")

		if not check_keys(id):
			id = input("Introduce a valid identifier name or 'list' for list all identifiers: ")
	return id

def print_decrypt_content():
	id = id_or_list()

	content = construct_dict()
	output = input('Copy Key (k) or Value (v) to clipboard? (N/k/v): ' )
	if output.lower() == 'k': os.system("echo '{}' | pbcopy".format(content[id][0]))
	if output.lower() == 'v': os.system("echo '{}' | pbcopy".format(content[id][1]))
	output = input('Show key/value pair? (N/y): ' )
	if output.lower() == 'y': print('Key:',content[id][0],'\nValue:',content[id][1])

def add_content(id, key,value):
	old_content = str(decrypt_content())
	new_content = old_content + '\n--!--\n' + id + '\n--!--\n' + key + '\n--!--\n' + value
	if check_keys(key):
		print("The key exist, please use other")
	else:
		encrypt_content(new_content)

def modify_content():
	content = construct_dict()
	id = id_or_list()
	content.pop(id, None)
	key = input("Introduce a key: ")
	value = input("Introduce a value: ")
	add_content(id, key, value)
	print("Done!")

def open_read_file(file):
	file = open('secrets', 'a+')
	file.seek(0)
	return file

def write_in_file(file, content):
	file.write(content)
	file.close()

def check_keys(id):
	return id in construct_dict()

def show_keys():
	for k,v in construct_dict().items():
		print(k)

def construct_dict():
	content = str(decrypt_content()).split('\n--!--\n')
	dictionary = {}
	index = 0
	while index < (len(content)):
		dictionary[content[index]] = [content[index+1],content[index+2]]
		index = index + 3
	return dictionary

def initialize():
	file  = open('secrets', 'w+')
	id = input('Introduce an Identifier: ')
	key = input('Introduce a Key: ')
	value = input('Introduce a Value: ')
	kv = id + '\n--!--\n' + key + '\n--!--\n' + value
	encrypt_content(kv)

def add_menu():
	file  = open('secrets', 'a+')
	kv = {}
	id = input('Introduce an Identifier: ').replace(' ','_')
	key = input('Introduce a Key: ')
	value = input('Introduce a Value: ')
	add_content(id, key,value)

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
		print('The file', FILE,'has not been found')
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
	else: interactive_menu()

if __name__ == "__main__":
	main(sys.argv[1:])
