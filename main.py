import gnupg
import sys
import os.path
import glob

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

def print_decrypt_content():
	key = input("Introduce the identifier name or 'list' for list all identifiers: ")
	while key.lower()=='list':
		show_keys()
		key = input("Introduce the identifier name or 'list' for list all identifiers: ")

	content = construct_dict()
	output = input('Copy Key or Value to clipboard? (N/k/v): ' )
	if output.lower() == 'k': os.system("echo '%s' | pbcopy" % content[key][0])
	if output.lower() == 'v': os.system("echo '%s' | pbcopy" % content[key][1])
	output = input('Show key/value pair? (N/y): ' )
	if output.lower() == 'y': print('Key: ',content[key][0],'\nValue: ',content[key][1])


def add_content(id, key,value):
	old_content = str(decrypt_content())
	new_content = old_content + '\n--!--\n' + id + '\n--!--\n' + key + '\n--!--\n' + value
	print(old_content)
	if check_keys(key):
		print("The key exist, please use other")
	else:
		encrypt_content(new_content)

def open_read_file(file):
	file = open('secrets', 'a+')
	file.seek(0)
	return file

def write_in_file(file,content):
	file.write(content)
	file.close()

def check_keys(new_key):
	return new_key in construct_dict()

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

def interactive():
	file  = open('secrets', 'a+')
	kv = {}
	id = input('Introduce an Identifier: ')
	key = input('Introduce a Key: ')
	value = input('Introduce a Value: ')
	add_content(id, key,value)

def exit():
	sys.exit(0)

def main(argv):
	if os.path.isfile(FILE):
		switcher = {
			0: lambda: '',
        		1: interactive,
        		2: print_decrypt_content,
        		3: show_keys,
        		4: exit
    		}
		option = int(input('\t1: Add Key/Value Pair\n\t2: Decrypt Key/Value Pair\n\t3: Show Keys\n\t4: Exit\nChoose: '))
		while option not in range(1, len(switcher)):
			option = int(input('Choose correct option: ' ))

		func = switcher.get(option, lambda: 'nothing')
		return func()
	else:
		initialize()

if __name__ == "__main__":
	main(sys.argv[1:])
